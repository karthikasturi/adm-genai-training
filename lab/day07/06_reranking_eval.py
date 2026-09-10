"""
EXERCISE 06 — Reranking: a second, more careful pass over the top-k results

CONCEPT
-------
A plain similarity search stays cheap by comparing the query's vector
against every stored vector INDEPENDENTLY - it never actually looks at
the query and a candidate together. That speed is what makes searching
thousands of chunks in milliseconds possible, but it also means the
ranking of the top few results is sometimes wrong: a chunk that's
generally on-topic can outrank one that specifically answers the
question, especially when an exact term (a rate-plan code, a proper
noun) matters and an embedding's paraphrase-tolerance works against it.

A RERANKER fixes this with a second, more expensive pass: it looks at the
query and ONE candidate chunk TOGETHER and scores that specific pair,
which is much more accurate but far too slow to run over an entire
collection - so it only ever runs on the small top-k set a similarity
search already narrowed things down to. A dedicated cross-encoder model
is the production-typical choice; today's version uses the same chat
model already provisioned, asked for a structured 0-10 relevance score -
Day 12's guardrailed, schema-constrained output pattern, applied to a new
job, and a choice made specifically to avoid needing a new vendor account
or network domain this course's whitelist doesn't include.

RUNNING SCENARIO
-----------------
Comparing plain similarity search against LLM-based reranking on a small
set of guest questions, to see where the two orderings actually differ.

SETUP
-----
    pip install openai chromadb pydantic python-dotenv
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the chunked document set and a small query set. Nothing to change
# here.
# =============================================================================

# [Placeholder — replace with your team's actual Sprint 3 reference documents]
CHUNKS = [
    "Pet Policy: Guests are welcome to bring pets to all outdoor dining areas and to designated pet-friendly rooms on the ground floor. A one-time pet fee of 35 USD applies per stay.",
    "Checkout Policy: Standard checkout time is 11:00 AM. Late checkout until 1:00 PM may be arranged with the front desk at no charge, subject to availability.",
    "Cancellation Policy: Cancellations made more than 48 hours before check-in receive a full refund. Cancellations made within 48 hours are charged for one night's stay.",
    "Spa Hours: The spa is open daily from 8:00 AM to 9:00 PM. A 24-hour cancellation notice is required to avoid a fee equal to 50 percent of the treatment price.",
    "Wi-Fi Access: Wi-Fi is complimentary in all rooms and public areas. The network name and password are printed on the welcome card left in every room at check-in.",
]

# A small query set - deliberately including one question where an exact
# term (spa cancellation vs. reservation cancellation) can trip up a
# plain similarity search.
QUERY_SET = [
    "What's the cancellation policy if I need to cancel my spa treatment?",
    "Can I bring my dog to the restaurant?",
    "How much does checking out late cost?",
]

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "openai:gpt-5.4-mini"

# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and clients.
#   from openai import OpenAI
#   import chromadb
#   from pydantic import BaseModel, Field
#   from langchain.chat_models import init_chat_model
#   client = OpenAI()
#   chroma_client = chromadb.Client()
#   model = init_chat_model(CHAT_MODEL)
from openai import OpenAI
import chromadb
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

client = OpenAI()
chroma_client = chromadb.Client()
model = init_chat_model(CHAT_MODEL)


# STEP 1 — load CHUNKS into a Chroma collection (cosine space), same
# pattern as exercises 02-03.
collection = chroma_client.create_collection(
    name="rerank_docs", metadata={"hnsw:space": "cosine"}
)
chunk_response = client.embeddings.create(model=EMBEDDING_MODEL, input=CHUNKS)
collection.add(
    ids=[f"chunk_{i}" for i in range(len(CHUNKS))],
    documents=CHUNKS,
    embeddings=[item.embedding for item in chunk_response.data],
)


# STEP 2 — define the structured score a pydantic BaseModel named
# RelevanceScore, with a score: int field (0-10) and a reasoning: str
# field, each with a Field(description=...) explaining what it means.
class RelevanceScore(BaseModel):
    score: int = Field(description="Relevance of the chunk to the query, 0 (irrelevant) to 10 (directly answers it)")
    reasoning: str = Field(description="One sentence explaining the score")


# STEP 3 — bind structured output to the model:
#   scoring_model = model.with_structured_output(RelevanceScore)
scoring_model = model.with_structured_output(RelevanceScore)


# STEP 4 — write llm_rerank(query: str, candidates: list[str], top_n: int = 3)
# -> list[str]: for each candidate, build a prompt containing the query and
# that one candidate, call scoring_model.invoke(prompt), collect
# (result.score, candidate) pairs, sort by score descending, and return
# the top_n candidates' text.
def llm_rerank(query: str, candidates: list[str], top_n: int = 3) -> list[str]:
    scored = []
    for chunk in candidates:
        prompt = (
            f"Query: {query}\n\nCandidate passage: {chunk}\n\n"
            "Score how well this passage answers the query."
        )
        result = scoring_model.invoke(prompt)
        scored.append((result.score, chunk))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [chunk for _, chunk in scored[:top_n]]


# STEP 5 — for each query in QUERY_SET:
#   - run collection.query(query_texts=[query], n_results=5) - deliberately
#     wider than usual, so reranking has room to reorder
#   - print the plain-similarity-search top 3 (the first 3 of the 5
#     returned documents, already ranked by distance)
#   - call llm_rerank(query, <all 5 returned documents>, top_n=3) and print
#     its top 3
#   - compare the two lists by eye
for query in QUERY_SET:
    results = collection.query(query_texts=[query], n_results=5)
    candidates = results["documents"][0]

    print(f"\n=== Query: {query} ===")
    print("Plain similarity search (top 3):")
    for doc in candidates[:3]:
        print(f"  - {doc[:70]}...")

    reranked = llm_rerank(query, candidates, top_n=3)
    print("LLM reranked (top 3):")
    for doc in reranked:
        print(f"  - {doc[:70]}...")

# What this demonstrates:
# Both lists are drawn from the SAME 5 candidates - reranking never adds a
# chunk the similarity search didn't already retrieve, it only reorders
# what's there. Look for the query where the two top-3 lists actually
# differ: that's a case where the plain vector-to-vector comparison
# ranked something lower than it deserved, and the reranker's closer,
# pair-by-pair look corrected it. If every query's two lists match
# exactly, try a query set with more exact-term or closely-related
# candidates - a genuinely useful evaluation needs at least one case where
# the plain search struggles.
