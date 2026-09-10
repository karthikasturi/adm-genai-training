"""
EXERCISE 02 — Loading embeddings into a vector database

CONCEPT
-------
Exercise 01's plain Python loop works for five documents held in memory.
It stops working the moment a team needs to add or remove documents
without recomputing every embedding, persist embeddings across a
restart, or filter results by another field while searching - the same
reason a real application reaches for a database instead of a plain
list. A VECTOR DATABASE stores each embedding alongside its source text
and metadata, and is built to answer "which stored documents are closest
to this query" efficiently, at a scale a Python loop can't keep up with.

Today's database is Chroma, run embedded (in-process, no server) - the
self-hosted option this course's own network whitelist actually
supports, since it has no vector-database SaaS domain on it.

One setting matters more than it looks: Chroma's OWN default distance
metric is `l2` (squared Euclidean distance), not cosine. OpenAI's
embeddings are normalized to length 1 specifically so that COSINE
similarity is the right comparison - so the collection below sets
`metadata={"hnsw:space": "cosine"}` explicitly, at creation time (this
cannot be changed on an existing collection afterward).

RUNNING SCENARIO
-----------------
Loading your reference-document set into a real, queryable, persistent
vector database instead of a Python list.

SETUP
-----
    pip install openai chromadb python-dotenv
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the same document set as exercise 01. Nothing to change here.
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

EMBEDDING_MODEL = "text-embedding-3-small"

# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and clients.
#   from openai import OpenAI
#   import chromadb
#   client = OpenAI()
#   chroma_client = chromadb.Client()   # in-memory for this exercise; a
#   # chromadb.PersistentClient(path="./chroma_data") instead would survive
#   # a process restart
from openai import OpenAI
import chromadb

client = OpenAI()
chroma_client = chromadb.Client()


# STEP 1 — create a collection named "hospitality_docs", explicitly
# configured for cosine similarity:
#   collection = chroma_client.create_collection(
#       name="hospitality_docs",
#       metadata={"hnsw:space": "cosine"},
#   )
collection = chroma_client.create_collection(
    name="hospitality_docs",
    metadata={"hnsw:space": "cosine"},
)


# STEP 2 — embed every document in DOCUMENTS with one batched
# client.embeddings.create(model=EMBEDDING_MODEL, input=DOCUMENTS) call,
# and collect the vectors into a plain list, in the same order as
# DOCUMENTS.
response = client.embeddings.create(model=EMBEDDING_MODEL, input=DOCUMENTS)
embeddings = [item.embedding for item in response.data]


# STEP 3 — load everything into the collection:
#   collection.add(ids=DOCUMENT_IDS, documents=DOCUMENTS, embeddings=embeddings)
# ids, documents, and embeddings must all be the same length and in the
# same order - a mismatch silently pairs the wrong embedding with the
# wrong text.
collection.add(ids=DOCUMENT_IDS, documents=DOCUMENTS, embeddings=embeddings)


# STEP 4 — confirm the load worked: print collection.count() and check it
# equals len(DOCUMENTS).
print("Collection count:", collection.count())


# STEP 5 — fetch one document back by its ID to confirm the round trip
# worked end to end: collection.get(ids=["policy_pets"]) and print the
# result's "documents" list.
fetched = collection.get(ids=["policy_pets"])
print("Fetched by ID:", fetched["documents"])

# What this demonstrates:
# The collection now holds every document's text, its embedding, and its
# ID together, persisted inside Chroma's own storage rather than a
# Python variable that disappears when the script ends (a
# PersistentClient would keep it on disk between runs). Exercise 03 picks
# up from here and actually queries it.
