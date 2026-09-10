"""
EXERCISE 01 — Generating embeddings: vector representations of text

CONCEPT
-------
Day 15's chain can already look up ONE specific record by an exact key
(get_reservation(reservation_id)) - the same thing a SQL
`WHERE id = ?` query does. It can't answer "Is the restaurant
pet-friendly?" when the actual policy text says "animals are welcome" -
there's no exact key to look up, and a `LIKE '%pet%'` search finds
nothing because the word "pet" never actually appears. An EMBEDDING is a
fixed-length list of numbers (a vector) generated from a piece of text,
such that text with similar MEANING produces vectors that are close
together - even when the wording is completely different.

RUNNING SCENARIO (used across this whole exercise set)
--------------------------------------------------------
Your capstone's Sprint 3 RAG assistant needs to answer guest questions
from a small set of hospitality reference documents (policy, amenities,
menu, listing, or lease text, depending on your team's brief).
# [Placeholder — replace with your team's actual Sprint 3 reference documents]

SETUP
-----
    pip install openai python-dotenv
    export OPENAI_API_KEY=...
(Embeddings use OpenAI specifically in this exercise set - Anthropic does
not offer its own embedding model and documents Voyage AI as its
recommended third-party provider instead, and Voyage AI isn't on this
course's whitelisted network. Your chat model in later exercises can
still be Anthropic's; only the embedding step itself calls OpenAI.)
"""

# =============================================================================
# GIVEN — a small hospitality reference-document set. Nothing to change here.
# =============================================================================

# [Placeholder — replace with your team's actual Sprint 3 reference documents]
DOCUMENTS = [
    "Guests are welcome to bring pets to all outdoor dining areas.",
    "Standard checkout time is 11:00 AM; late checkout may be arranged with the front desk.",
    "Cancellations made more than 48 hours before check-in receive a full refund.",
    "The spa is open daily from 8:00 AM to 9:00 PM, with treatments bookable online.",
    "Wi-Fi is complimentary in all rooms; the network name and password are on the welcome card.",
]

# A guest question deliberately worded differently from any document above -
# no shared exact wording with DOCUMENTS[0], only shared meaning.
GUEST_QUESTION = "Can I bring my dog to the restaurant?"

EMBEDDING_MODEL = "text-embedding-3-small"  # 1536 dimensions by default

# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and client.
#   from openai import OpenAI
#   client = OpenAI()
from openai import OpenAI
client = OpenAI()


# STEP 1 — embed ONE document: call
#   client.embeddings.create(model=EMBEDDING_MODEL, input=DOCUMENTS[0])
# and store the result. The vector itself lives at response.data[0].embedding.
response = client.embeddings.create(model=EMBEDDING_MODEL, input=DOCUMENTS[0])
vector = response.data[0].embedding


# STEP 2 — confirm the vector's shape: print len(vector). It should be 1536,
# text-embedding-3-small's default dimension count - the same number for
# every input, no matter how long or short the text.
print("Vector length:", len(vector))


# STEP 3 — embed EVERY document in DOCUMENTS (a loop, or a single batched
# call with input=DOCUMENTS - the API accepts a list). Store each resulting
# vector alongside its original text, e.g. a list of
# {"text": ..., "embedding": ...} dictionaries, in the same order as
# DOCUMENTS.
batch_response = client.embeddings.create(model=EMBEDDING_MODEL, input=DOCUMENTS)
embedded_docs = [
    {"text": text, "embedding": item.embedding}
    for text, item in zip(DOCUMENTS, batch_response.data)
]
print(f"Embedded {len(embedded_docs)} documents.")


# STEP 4 — embed GUEST_QUESTION the same way (one call, one input string).
question_response = client.embeddings.create(model=EMBEDDING_MODEL, input=GUEST_QUESTION)
question_vector = question_response.data[0].embedding


# STEP 5 — write a plain-Python cosine_similarity(a, b) function (no
# library needed): dot product of a and b, divided by the product of their
# two magnitudes. Use it to compare question_vector against EVERY vector in
# embedded_docs, and print each document's text next to its similarity
# score, most similar first.
import math

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    return dot / (mag_a * mag_b)

scored = [
    (cosine_similarity(question_vector, doc["embedding"]), doc["text"])
    for doc in embedded_docs
]
scored.sort(key=lambda pair: pair[0], reverse=True)
for score, text in scored:
    print(f"{score:.4f}  {text}")

# What this demonstrates:
# GUEST_QUESTION shares almost no literal words with DOCUMENTS[0] ("bring
# my dog to the restaurant" vs. "bring pets to all outdoor dining areas"),
# yet cosine similarity ranks it highest - proof this is a MEANING-based
# match, not a keyword match. This is the exact comparison a vector
# database (exercises 02-03) does internally, at scale, instead of the plain
# Python loop above.
