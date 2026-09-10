"""
EXERCISE 03 — Similarity search: querying a vector database and inspecting results

CONCEPT
-------
Exercise 02 loaded a collection; this exercise asks it the actual
question a guest would ask, and inspects what comes back. A SIMILARITY
SEARCH is not an exact match and not a keyword pattern match - it's a
ranked answer to "which stored pieces of text are closest in MEANING to
this query," using the same cosine comparison exercise 01 computed by
hand, now run internally by Chroma against every stored document at
once.

RUNNING SCENARIO
-----------------
Asking your loaded collection a guest question worded differently from
any stored document's exact wording, and checking that the ranking
actually reflects meaning, not shared words.

SETUP
-----
    pip install openai chromadb python-dotenv
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the same document set as exercises 01-02. Nothing to change here.
# =============================================================================

# [Placeholder — replace with your team's actual Sprint 3 reference documents]
DOCUMENTS = [
    "Guests are welcome to bring pets to all outdoor dining areas.",
    "Standard checkout time is 11:00 AM; late checkout may be arranged with the front desk.",
    "Cancellations made more than 48 hours before check-in receive a full refund.",
    "The spa is open daily from 8:00 AM to 9:00 PM, with treatments bookable online.",
    "Wi-Fi is complimentary in all rooms; the network name and password are on the welcome card.",
]
DOCUMENT_IDS = ["policy_pets", "policy_checkout", "policy_cancellation", "spa_hours", "wifi"]

# Worded differently from DOCUMENTS[0] on purpose - no shared exact wording,
# only shared meaning.
GUEST_QUESTION = "Can I bring my dog to the restaurant?"

EMBEDDING_MODEL = "text-embedding-3-small"

# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports, clients, and re-loading the collection (standalone
# file - rebuild exercise 02's collection here rather than importing it).
from openai import OpenAI
import chromadb

client = OpenAI()
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="hospitality_docs",
    metadata={"hnsw:space": "cosine"},
)
_response = client.embeddings.create(model=EMBEDDING_MODEL, input=DOCUMENTS)
collection.add(
    ids=DOCUMENT_IDS,
    documents=DOCUMENTS,
    embeddings=[item.embedding for item in _response.data],
)


# STEP 1 — run a similarity search for GUEST_QUESTION, asking for the top
# 3 results:
#   results = collection.query(query_texts=[GUEST_QUESTION], n_results=3)
# (Chroma calls its own embedding function on query_texts automatically -
# you don't have to embed the query yourself the way exercise 01 did.)
results = collection.query(query_texts=[GUEST_QUESTION], n_results=3)


# STEP 2 — print each returned document's text next to its distance
# score and its ID, most similar first. results["documents"][0],
# results["distances"][0], and results["ids"][0] are parallel lists, in
# ranked order.
for doc_id, doc, distance in zip(
    results["ids"][0], results["documents"][0], results["distances"][0]
):
    print(f"{distance:.4f}  [{doc_id}]  {doc}")


# STEP 3 — by eye, compare GUEST_QUESTION's wording to the top-ranked
# result's actual text (print them side by side if it helps). Confirm
# they share meaning ("dog" / "restaurant" vs. "pets" / "outdoor dining")
# even though they share almost no exact words.
print("\nQuestion: ", GUEST_QUESTION)
print("Top match:", results["documents"][0][0])


# STEP 4 — run a SECOND query, this time using words that appear in NONE
# of the documents at all (for example, "Do you have a gym?"), and print
# its results too. Notice that Chroma still returns its top 3 closest
# matches - a similarity search always returns its best available
# matches, even when none of them are actually a good answer, which is
# exactly why Module 16B later adds a reranking and evaluation step
# rather than trusting a raw similarity search's top result blindly.
no_match_results = collection.query(query_texts=["Do you have a gym?"], n_results=3)
print("\nQuestion with no real answer in the documents:")
for doc, distance in zip(no_match_results["documents"][0], no_match_results["distances"][0]):
    print(f"{distance:.4f}  {doc}")

# What this demonstrates:
# The first query's top result is a genuine meaning-based match, proving
# the search works the way exercise 01 predicted by hand. The second
# query's results are a useful warning: a vector database always returns
# its closest matches, even if "closest" still isn't actually close - a
# similarity search has no built-in concept of "none of these are good
# enough," which is a real limitation this course's later reranking and
# evaluation work exists to address.
