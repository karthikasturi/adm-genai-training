"""
EXERCISE 07 — Composing a RAG chain with LangChain Expression Language (LCEL)

CONCEPT
-------
Exercise 05 built retrieve-then-generate as a hand-written Python function:
call retriever.invoke(), join the results into a string, format a prompt,
call model.invoke(), return .content. That function works, but it's opaque
to LangChain itself - the framework has no idea retrieval and generation
are two steps of one pipeline, so the function gets none of what a
LangChain-native object gets for free: streaming tokens as they're
generated, running several inputs concurrently with automatic batching, or
swapping one step out without touching the rest.

LCEL (LangChain Expression Language) composes each step as a Runnable and
chains them with the `|` pipe operator, so the chain itself is a first-class
LangChain object instead of a plain function:

    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()

A dict literal used with `|` is automatically treated as a RunnableParallel
(runs each entry against the same input, here the incoming question);
`retriever | format_docs` chains a retriever into a plain join function; the
combined dict feeds a prompt, then the model, then a string parser. Every
step is swappable, and the finished chain supports .invoke(), .batch(), and
.stream() automatically, without writing any of that plumbing by hand.

SCOPE NOTE - what this exercise is (and isn't)
------------------------------------------------
LangChain previously shipped ready-made create_stuff_documents_chain /
create_retrieval_chain helpers for exactly this job; as of the current
major LangChain version those moved into the langchain_classic package as
a legacy surface, so this exercise builds the equivalent chain directly
from langchain_core's still-current Runnable primitives instead, confirmed
against LangChain's own current reference documentation.

LangChain's own current documentation also frames this whole exercise as
just one of three RAG shapes: this is "2-step RAG" (retrieve, then
generate, in a fixed order). The other shape it names is "agentic RAG," a
tool-calling agent that decides FOR ITSELF when to retrieve and with what
query. That's not an accident of scope here - it's exactly Day 17 / Module
17A's job next: taking exercise 05's RAG tool (the plain-function version)
and wiring it into a decision loop a model drives. This exercise stays
within 2-step RAG on purpose.

RUNNING SCENARIO
-----------------
The same retrieve-then-answer job as exercise 05, rebuilt as a single
composed LCEL chain instead of a hand-written function, so the two
implementations can be compared directly.

SETUP
-----
    pip install langchain langchain-openai langchain-chroma langgraph python-dotenv
    export OPENAI_API_KEY=...      # embeddings (and optionally chat)
    export ANTHROPIC_API_KEY=...   # optional, for the chat model instead
"""

# =============================================================================
# GIVEN — the same chunked document set and sample questions as exercise 05.
# Nothing to change here.
# =============================================================================

# [Placeholder — replace with your team's actual Sprint 3 reference documents]
CHUNKS = [
    "Pet Policy: Guests are welcome to bring pets to all outdoor dining areas and to designated pet-friendly rooms on the ground floor. A one-time pet fee of 35 USD applies per stay.",
    "Checkout Policy: Standard checkout time is 11:00 AM. Late checkout until 1:00 PM may be arranged with the front desk at no charge, subject to availability.",
    "Cancellation Policy: Cancellations made more than 48 hours before check-in receive a full refund. Cancellations made within 48 hours are charged for one night's stay.",
    "Spa Hours: The spa is open daily from 8:00 AM to 9:00 PM. A 24-hour cancellation notice is required to avoid a fee equal to 50 percent of the treatment price.",
    "Wi-Fi Access: Wi-Fi is complimentary in all rooms and public areas. The network name and password are printed on the welcome card left in every room at check-in.",
]

SAMPLE_QUESTIONS = [
    "Can I bring my dog to the restaurant?",
    "What's the cancellation policy for a spa treatment?",
    "Is there a fee for checking out late?",
]

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"

# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and model.
#   from langchain_openai import OpenAIEmbeddings
#   from langchain_chroma import Chroma
#   from langchain_core.prompts import ChatPromptTemplate
#   from langchain_core.output_parsers import StrOutputParser
#   from langchain_core.runnables import RunnablePassthrough
#   from langchain.chat_models import init_chat_model
#   model = init_chat_model(CHAT_MODEL)
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import init_chat_model

model = init_chat_model(CHAT_MODEL)


# STEP 1 — build the vector store and retriever, same pattern as exercise
# 05: an OpenAIEmbeddings object, a Chroma vectorstore
# (collection_name="lcel_hospitality_docs", collection_metadata={"hnsw:space":
# "cosine"}), load CHUNKS with vectorstore.add_texts(CHUNKS), then
# vectorstore.as_retriever(search_kwargs={"k": 3}).
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    collection_name="lcel_hospitality_docs",
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"},
)
vectorstore.add_texts(CHUNKS)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# STEP 2 — a plain function format_docs(docs) -> str that joins each
# retrieved Document's .page_content with "\n\n". This is the piece that
# gets slotted into the chain with `retriever | format_docs` in Step 4 -
# LangChain automatically wraps a plain function used with `|` as a
# RunnableLambda.
def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


# STEP 3 — the same answer instruction as exercise 05, as a
# ChatPromptTemplate (the chat-oriented template class, since this chain
# pipes straight into a chat model rather than formatting a plain string
# first):
#   answer_prompt = ChatPromptTemplate.from_template(
#       "Answer the guest's question using ONLY the context below. "
#       "If the context doesn't contain the answer, say you're not sure.\n\n"
#       "Context:\n{context}\n\nGuest question: {question}"
#   )
answer_prompt = ChatPromptTemplate.from_template(
    "Answer the guest's question using ONLY the context below. "
    "If the context doesn't contain the answer, say you're not sure.\n\n"
    "Context:\n{context}\n\nGuest question: {question}"
)


# STEP 4 — compose the chain with the `|` pipe operator: a dict mapping
# "context" to `retriever | format_docs` and "question" to
# RunnablePassthrough() (so the raw incoming question reaches the prompt
# unchanged), piped into answer_prompt, then model, then StrOutputParser()
# to unwrap the plain text of the model's reply.
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | answer_prompt
    | model
    | StrOutputParser()
)


# STEP 5 — run the chain the same way exercise 05's rag_answer() was
# called: rag_chain.invoke(question) for each question in
# SAMPLE_QUESTIONS, printing question and answer. Compare against exercise
# 05's output for the same questions - the answers should be equivalent,
# built from the identical retrieve-then-generate steps, just composed
# declaratively instead of imperatively.
for question in SAMPLE_QUESTIONS:
    answer = rag_chain.invoke(question)
    print(f"Q: {question}\nA: {answer}\n")


# STEP 6 — what exercise 05's plain function COULDN'T do for free: stream
# the first question's answer token by token with rag_chain.stream(question),
# printing each chunk as it arrives instead of waiting for the full reply.
print("=== Streaming the first question's answer ===")
for chunk in rag_chain.stream(SAMPLE_QUESTIONS[0]):
    print(chunk, end="", flush=True)
print("\n")


# STEP 7 — run all of SAMPLE_QUESTIONS through rag_chain.batch(...) in one
# call instead of exercise 05's for-loop, and print each result. batch()
# runs the questions concurrently rather than one at a time - a second
# thing this chain gets automatically just by being composed as a Runnable.
print("=== Batching all sample questions ===")
batch_answers = rag_chain.batch(SAMPLE_QUESTIONS)
for question, answer in zip(SAMPLE_QUESTIONS, batch_answers):
    print(f"Q: {question}\nA: {answer}\n")

# What this demonstrates:
# rag_chain.invoke(), .stream(), and .batch() all work without writing any
# streaming or batching logic - that's what composing the pipeline as
# Runnables buys over exercise 05's hand-written function, which only ever
# supports the one calling style it was written for. The retrieve-then-
# generate LOGIC is identical between the two exercises; what changed is
# how it's assembled. Wrapping rag_chain.invoke as a plain function and
# decorating it with @tool would make this pipeline just as pluggable into
# Day 15's chain as exercise 05's version - that step is deliberately left
# out here since exercise 05 already covers it. What's genuinely new next
# is Day 17 / Module 17A: handing this same retrieval tool to an agent that
# decides on its own when to call it, instead of the fixed
# retrieve-then-generate order both exercise 05 and this file always run in.
