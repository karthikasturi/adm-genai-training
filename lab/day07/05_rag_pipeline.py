"""
EXERCISE 05 — Retrieval pipeline: combining a retriever with a generator

CONCEPT
-------
A similarity search returns raw chunks of text, ranked by relevance, and
stops there - it doesn't turn those chunks into an answer a guest would
recognize as a reply. RETRIEVAL-AUGMENTED GENERATION composes two pieces:
a RETRIEVER (everything exercises 01-03 built) and a GENERATOR (the same
chat model from Day 15's chain), so the model answers using retrieved,
grounded context instead of guessing from training knowledge alone - the
open-book-exam version of a model call, not the closed-book one.

LangChain's `Chroma` vectorstore wraps a collection with an
`as_retriever()` method, turning it into a standard retriever a chain can
call as one step - the same role get_reservation played in Day 15's
tool-integration exercise, just returning relevant document chunks
instead of one specific record. The prompt's own instruction to answer
"using ONLY the context below" is doing real work: it's Day 12's
guardrail discipline, applied here to stop the model from quietly
falling back on its own (possibly wrong) training knowledge when the
retrieved context doesn't actually answer the question.

RUNNING SCENARIO
-----------------
Your capstone's actual Sprint 3 RAG feature: a tool-wrapped function that
retrieves from your reference documents and drafts a grounded reply.
# [Placeholder — replace with your team's actual Sprint 3 AI feature]

SETUP
-----
    pip install langchain langchain-openai langchain-chroma langgraph python-dotenv
    export OPENAI_API_KEY=...      # embeddings (and optionally chat)
    export ANTHROPIC_API_KEY=...   # optional, for the chat model instead
"""

# =============================================================================
# GIVEN — the chunked document set from exercise 04. Nothing to change here.
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
#   from langchain_core.prompts import PromptTemplate
#   from langchain.chat_models import init_chat_model
#   from langchain.tools import tool
#   model = init_chat_model(CHAT_MODEL)
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool

model = init_chat_model(CHAT_MODEL)


# STEP 1 — build the vector store: create an OpenAIEmbeddings object
# (model=EMBEDDING_MODEL), then a Chroma vectorstore with
# collection_name="hospitality_docs", embedding_function=<your
# OpenAIEmbeddings>, and collection_metadata={"hnsw:space": "cosine"}.
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    collection_name="hospitality_docs",
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"},
)


# STEP 2 — load CHUNKS into the vectorstore with vectorstore.add_texts(CHUNKS),
# then build a retriever: vectorstore.as_retriever(search_kwargs={"k": 3}).
vectorstore.add_texts(CHUNKS)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# STEP 3 — write the answer template: a PromptTemplate instructing the
# model to answer strictly from the retrieved context and say so plainly
# when the context doesn't contain an answer.
#   answer_template = PromptTemplate.from_template(
#       "Answer the guest's question using ONLY the context below. "
#       "If the context doesn't contain the answer, say you're not sure.\n\n"
#       "Context:\n{context}\n\nGuest question: {question}"
#   )
answer_template = PromptTemplate.from_template(
    "Answer the guest's question using ONLY the context below. "
    "If the context doesn't contain the answer, say you're not sure.\n\n"
    "Context:\n{context}\n\nGuest question: {question}"
)


# STEP 4 — write a plain function rag_answer(question: str) -> str that:
#   - retrieves with retriever.invoke(question)
#   - joins the retrieved docs' .page_content with "\n\n" into one context string
#   - formats answer_template with {"context": context, "question": question}
#   - returns model.invoke(prompt).content
def rag_answer(question: str) -> str:
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = answer_template.invoke({"context": context, "question": question})
    return model.invoke(prompt).content


# STEP 5 — wrap rag_answer as a tool, exactly like get_reservation in
# Day 15's tool-integration exercise:
#   @tool
#   def answer_guest_question(question: str) -> str:
#       """Answer a guest's question using the hotel's reference documents.
#
#       Use this for any question about policies, amenities, hours, or
#       other information found in the property's own documents.
#       """
#       return rag_answer(question)
@tool
def answer_guest_question(question: str) -> str:
    """Answer a guest's question using the hotel's reference documents.

    Use this for any question about policies, amenities, hours, or
    other information found in the property's own documents.
    """
    return rag_answer(question)


# STEP 6 — invoke answer_guest_question.invoke(...) (a @tool-decorated
# function is called with .invoke(), same as Day 15's tool exercises) with
# each question in SAMPLE_QUESTIONS, and print the question and its answer.
for question in SAMPLE_QUESTIONS:
    answer = answer_guest_question.invoke(question)
    print(f"Q: {question}\nA: {answer}\n")

# What this demonstrates:
# answer_guest_question is now a complete, callable RAG tool - retriever
# plus generator, wrapped exactly the way Day 15's get_reservation tool
# was wrapped. Bind it to your Day 15 chain's model with bind_tools([...])
# and it plugs into that same graph as one more node, precisely the
# connection named in the sequencing table: this RAG pipeline becomes a
# callable tool on the tool-calling chain already built.
