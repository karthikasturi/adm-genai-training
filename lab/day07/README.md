# Day 16 — RAG stack, vector databases & retrieval exercises

Seven standalone exercises, one RAG-stack concept per file. Each file uses
the same running scenario for continuity: a small set of hospitality
reference documents (policy, amenities, menu, listing, or lease text,
depending on your team's brief) that a guest-facing assistant needs to
answer questions from. It's a stand-in for your own Sprint 3 RAG
assistant — wherever you see
`# [Placeholder — replace with your team's actual Sprint 3 reference documents]`,
that's the spot to swap in your own.

This builds directly on Day 15's chain and tool-integration work
(`lab/day06`): exercise 05 wraps a finished retrieval pipeline with
`@tool`, exactly the way `05_tool_integration.py` wrapped
`get_reservation` — the retrieval pipeline built here is meant to plug
into that same chain as one more callable tool, not to replace it.

## Format

Each file is fully standalone (no shared code between files) and split
into two sections:

- **GIVEN** — the sample documents, queries, and (from exercise 06 on)
  scoring schemas, already written out. You don't need to design these
  yourself.
- **YOUR TURN** — numbered `# STEP` comments describing what the code
  needs to do, with the exact library, class, and method names to use.
  The code is filled in under each step so you can run the file directly
  and see what it does, then re-read each step's comment to understand
  *why* that call is there.

There are no separate answer files — the steps and the code live
together in each file.

## Setup

```bash
cd lab/day07
pip install -r requirements.txt
cp .env.example .env
# edit .env and fill in OPENAI_API_KEY (required — see "A note on embeddings"
# below) and, optionally, ANTHROPIC_API_KEY
```

## Exercise order

| File | Concept |
|---|---|
| `01_generate_embeddings.py` | Embeddings — generating vector representations of text |
| `02_load_vector_database.py` | Loading embeddings into a self-hosted Chroma vector database |
| `03_similarity_search.py` | Running a similarity search query and inspecting the results |
| `04_chunking_comparison.py` | `RecursiveCharacterTextSplitter` — chunking, and comparing retrieval before/after |
| `05_rag_pipeline.py` | Assembling a full RAG pipeline: a retriever plus a generator, wrapped as a tool |
| `06_reranking_eval.py` | LLM-based reranking, evaluated against plain similarity search on a small query set |
| `07_lcel_rag_chain.py` | Composing exercise 05's retriever + generator as a single LCEL chain (`invoke`/`stream`/`batch`) |

Work through them in order — `02` and `03` both build on `01`'s embedding
call, `04`'s chunked documents are what `05` actually loads and retrieves
from, `06` reruns `03`'s plain similarity search side by side with a
reranked version of the same candidates, and `07` rebuilds `05`'s
hand-written retrieve-then-generate function as a single composed LCEL
chain, to compare the two ways of assembling the same pipeline.

## A note on embeddings and vendor choice

Every other day in this program treats OpenAI and Anthropic as an
interchangeable choice for your chat model. Embeddings are the one place
that's genuinely not true: Anthropic's own documentation states plainly
that "Anthropic does not offer its own embedding model," and instead
recommends a third-party provider, Voyage AI. Voyage AI's own API isn't
on this course's currently whitelisted network, so every exercise here
calls OpenAI's embeddings endpoint (`OPENAI_API_KEY` is required even if
your chat model, in exercises 05 and 06, is Anthropic's).

## A note on the vector database

Today's vector database is Chroma, run **embedded** — in the same Python
process, with no separate server and no account to create. This is a
deliberate choice for this course's own network policy (no hosted
vector-database SaaS domain is on the whitelist), not a claim that an
embedded database is the only correct choice for a real production
system. Every collection created below is explicitly configured for
**cosine** similarity (`metadata={"hnsw:space": "cosine"}`) rather than
left on Chroma's own default (`l2`), because OpenAI's embeddings are
normalized specifically for cosine comparison — leaving this setting on
the default is a common, easy-to-miss mistake.

## A note on hybrid search and reranking

Chroma's hosted Cloud product has a built-in hybrid (dense + keyword)
search with automatic score fusion — the self-hosted, embedded database
used here does not ship that feature. Exercise 06 builds the reranking
half of retrieval-quality improvement (a second, more careful pass over
an already-narrowed set of candidates) using the chat model you already
have provisioned, scored with the same guardrailed, structured-output
pattern from Day 12, rather than a dedicated cross-encoder reranker
model or a hosted rerank API — both would need a new vendor account or a
model download from a host outside this course's whitelisted network.

## A note on LCEL vs. agentic RAG

Exercise 07 composes exercise 05's retrieve-then-generate function as a
single LCEL (LangChain Expression Language) chain instead, using
`langchain_core`'s Runnable primitives (`RunnablePassthrough`, the `|`
pipe operator) rather than the older `create_stuff_documents_chain` /
`create_retrieval_chain` helpers — those moved into the `langchain_classic`
package as a legacy surface in the current LangChain major version, so
this exercise deliberately avoids teaching them as if current. LangChain's
own current documentation frames exercise 07's shape as "2-step RAG"
(retrieve, then generate, in a fixed order), distinct from "agentic RAG" (a
tool-calling agent decides for itself when and what to retrieve). Building
the agentic version — handing exercise 05's RAG tool to a decision loop a
model drives itself — is Day 17 / Module 17A's job next, not repeated here.
