"""
EXERCISE 04 — Chunking: splitting a long document to preserve retrieval quality

CONCEPT
-------
Exercises 01-02 used short, single-topic passages, one sentence each. A
REAL reference document usually isn't that tidy - it's several paragraphs
covering several different topics in one file. Embedding a whole
multi-topic document as ONE vector blurs all of its topics together (the
same "one prompt can't do a two-part job" problem, now at the
document-embedding level): a question about one specific topic has to
compete, inside that one blurred vector, against every other topic the
document also covers. CHUNKING splits a document into smaller pieces
BEFORE embedding each one separately, so each vector represents one
coherent, focused unit of meaning.

A naive fixed-size cut (every N characters, no matter what's there) can
slice a sentence in half. RecursiveCharacterTextSplitter improves on this:
it tries a list of separators from the most meaningful break down to the
least (paragraphs, then lines, then sentences, then words), so a chunk
boundary lands on a real structural break wherever one is available.
`chunk_overlap` repeats a small window of text between neighboring
chunks, so a fact sitting right at a boundary still appears in full in at
least one chunk.

RUNNING SCENARIO
-----------------
A longer, multi-topic excerpt of your team's own reference documents -
long enough that embedding it whole noticeably blurs its topics together.

SETUP
-----
    pip install openai chromadb langchain-text-splitters python-dotenv
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — a longer, multi-topic document. Nothing to change here.
# =============================================================================

# [Placeholder — replace with a longer excerpt of your team's actual
# Sprint 3 reference documents]
LONG_DOCUMENT = """
Pet Policy: Guests are welcome to bring pets to all outdoor dining areas
and to designated pet-friendly rooms on the ground floor. A one-time pet
fee of 35 USD applies per stay, and pets must remain leashed in all
common areas at all times.

Checkout Policy: Standard checkout time is 11:00 AM. Late checkout until
1:00 PM may be arranged with the front desk at no charge, subject to
availability; checkout after 1:00 PM is billed at half the nightly rate.

Cancellation Policy: Cancellations made more than 48 hours before
check-in receive a full refund. Cancellations made within 48 hours of
check-in are charged for one night's stay. No-shows are charged the full
reservation amount.

Spa Hours: The spa is open daily from 8:00 AM to 9:00 PM. Treatments can
be booked online up to 30 days in advance or by calling the spa desk
directly. A 24-hour cancellation notice is required to avoid a
cancellation fee equal to 50 percent of the treatment price.

Wi-Fi Access: Wi-Fi is complimentary in all rooms and public areas. The
network name and password are printed on the welcome card left in every
room at check-in, and can also be requested at the front desk at any
time.
""".strip()

# A question that targets exactly ONE of the topics above.
TEST_QUESTION = "What happens if I need to cancel my spa appointment?"

EMBEDDING_MODEL = "text-embedding-3-small"

# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and clients.
#   from openai import OpenAI
#   import chromadb
#   from langchain_text_splitters import RecursiveCharacterTextSplitter
#   client = OpenAI()
#   chroma_client = chromadb.Client()
from openai import OpenAI
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

client = OpenAI()
chroma_client = chromadb.Client()


# STEP 1 — BASELINE: embed LONG_DOCUMENT as a single whole-document chunk,
# and load it into a collection named "whole_document" (cosine space, per
# exercise 02's pattern) with one id, e.g. "full_doc".
whole_collection = chroma_client.create_collection(
    name="whole_document", metadata={"hnsw:space": "cosine"}
)
whole_response = client.embeddings.create(model=EMBEDDING_MODEL, input=LONG_DOCUMENT)
whole_collection.add(
    ids=["full_doc"],
    documents=[LONG_DOCUMENT],
    embeddings=[whole_response.data[0].embedding],
)


# STEP 2 — run TEST_QUESTION against the "whole_document" collection
# (collection.query(query_texts=[TEST_QUESTION], n_results=1)) and print
# the returned distance score. This is your "before chunking" baseline.
baseline_result = whole_collection.query(query_texts=[TEST_QUESTION], n_results=1)
baseline_distance = baseline_result["distances"][0][0]
print("BEFORE chunking - distance:", baseline_distance)


# STEP 3 — split LONG_DOCUMENT with RecursiveCharacterTextSplitter.
# Start with chunk_size=300, chunk_overlap=40, and adjust chunk_size if
# your own document's paragraphs are noticeably longer or shorter:
#   splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=40)
#   chunks = splitter.split_text(LONG_DOCUMENT)
# Print len(chunks) and each chunk, to see where the splitter actually cut.
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=40)
chunks = splitter.split_text(LONG_DOCUMENT)
print(f"Split into {len(chunks)} chunks:")
for i, chunk in enumerate(chunks):
    print(f"  chunk {i}: {chunk[:60]}...")


# STEP 4 — embed and load every chunk into a SECOND collection named
# "chunked_document" (cosine space), one chunk per id (e.g. "chunk_0",
# "chunk_1", ...).
chunked_collection = chroma_client.create_collection(
    name="chunked_document", metadata={"hnsw:space": "cosine"}
)
chunk_response = client.embeddings.create(model=EMBEDDING_MODEL, input=chunks)
chunked_collection.add(
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    documents=chunks,
    embeddings=[item.embedding for item in chunk_response.data],
)


# STEP 5 — run the SAME TEST_QUESTION against "chunked_document"
# (n_results=1) and print the returned distance score and the actual
# chunk text returned. This is your "after chunking" result.
chunked_result = chunked_collection.query(query_texts=[TEST_QUESTION], n_results=1)
chunked_distance = chunked_result["distances"][0][0]
chunked_text = chunked_result["documents"][0][0]
print("AFTER chunking - distance:", chunked_distance)
print("AFTER chunking - matched chunk:", chunked_text)


# STEP 6 — compare the two distance scores you printed in Steps 2 and 5.
# The chunked collection's score should be noticeably better (a smaller
# cosine distance = more similar), and its matched chunk should focus
# specifically on the spa/cancellation topic, not a blurred mix of all
# five policies.
print(f"\nImprovement: {baseline_distance:.4f} (whole doc) -> {chunked_distance:.4f} (chunked)")

# What this demonstrates:
# The whole-document embedding had to represent five unrelated policies in
# one vector, diluting its similarity to any single-topic question. Once
# each policy became its own chunk, the spa-cancellation chunk's vector
# represents ONLY that topic, and ranks noticeably closer to a question
# about exactly that topic. If your own numbers don't show a real
# difference, your chunk_size is probably still too large for this
# document - try a smaller one.
