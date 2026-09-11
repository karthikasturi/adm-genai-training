"""
EXERCISE 03 — Verifying the loop actually loops

CONCEPT
-------
Exercise 02 built a graph shaped like a loop - but a graph that compiles
correctly can still fail to actually exercise that loop if it's only ever
tested with a message that needs exactly one tool call. Testing only that
case can pass every structural check and still be, in behavior, identical
to Day 15's non-looping chain: one conditional edge, one tool call, done.

This exercise is deliberately a verification step, not a new mechanism: the
same compiled agent from exercise 02, run against TWO different kinds of
messages side by side, counting how many times call_model is actually
visited for each - the concrete proof that the backward edge does what it's
supposed to.

RUNNING SCENARIO
-----------------
The same agent from exercise 02, proven against a single-tool message and a
two-tool message, with the visit count for each printed and compared.

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the same two tools and compiled agent shape as exercise 02.
# Nothing to change here.
# =============================================================================

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
EMBEDDING_MODEL = "text-embedding-3-small"

model = init_chat_model(CHAT_MODEL)

SAMPLE_RESERVATIONS = {
    "214": "check_in=2026-09-20, status=confirmed",
    "310": "check_in=2026-09-25, status=pending",
}

@tool
def get_reservation(reservation_id: str) -> str:
    """Look up a reservation by ID and return its check-in date and status.

    Use this when a guest's request depends on the details of a specific, existing reservation rather than a general policy question.
    """
    return SAMPLE_RESERVATIONS.get(reservation_id, "no reservation found with that ID")

CHUNKS = [
    "Pet Policy: Guests are welcome to bring pets to all outdoor dining areas and to designated pet-friendly rooms on the ground floor. A one-time pet fee of 35 USD applies per stay.",
    "Checkout Policy: Standard checkout time is 11:00 AM. Late checkout until 1:00 PM may be arranged with the front desk at no charge, subject to availability.",
    "Cancellation Policy: Cancellations made more than 48 hours before check-in receive a full refund. Cancellations made within 48 hours are charged for one night's stay.",
    "Spa Hours: The spa is open daily from 8:00 AM to 9:00 PM. A 24-hour cancellation notice is required to avoid a fee equal to 50 percent of the treatment price.",
    "Wi-Fi Access: Wi-Fi is complimentary in all rooms and public areas. The network name and password are printed on the welcome card left in every room at check-in.",
]

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    collection_name="day08_ex03_hospitality_docs",
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"},
)
vectorstore.add_texts(CHUNKS)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

answer_prompt = PromptTemplate.from_template(
    "Answer the guest's question using ONLY the context below. "
    "If the context doesn't contain the answer, say you're not sure.\n\n"
    "Context:\n{context}\n\nGuest question: {question}"
)

def rag_answer(question: str) -> str:
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = answer_prompt.invoke({"context": context, "question": question})
    return model.invoke(prompt).content

@tool
def answer_guest_question(question: str) -> str:
    """Answer a guest's question using the hotel's reference documents.

    Use this for any question about policies, amenities, hours, or
    other information found in the property's own documents.
    """
    return rag_answer(question)

tools = [get_reservation, answer_guest_question]
model_with_tools = model.bind_tools(tools)

ONE_TOOL_MESSAGE = "Can you check the status of reservation 214 for me?"
TWO_TOOL_MESSAGE = "Can I get late checkout, and what does my reservation 214 say about check-out time?"

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — rebuild exercise 02's compiled agent here (standalone file, same
# pattern as day07's exercises rebuilding prior exercises' setup): AgentState
# with a messages field (Annotated[list, add_messages]), call_model (invoking
# model_with_tools, printing the decision, returning {"messages": [response]}),
# a ToolNode over `tools`, the graph with call_model + the tool node, a
# conditional edge via tools_condition, and the loop-closing edge back to
# call_model. Compile into `agent`.
# YOUR CODE HERE


# STEP 2 — write count_call_model_visits(message: str) -> int that:
#   - invokes agent with {"messages": [HumanMessage(content=message)]}
#   - counts how many messages in the FINAL state's "messages" list are
#     AIMessage instances (each one represents one pass through call_model -
#     import AIMessage from langchain_core.messages to check with isinstance)
#   - prints the message, the visit count, and every message's type and
#     content in order
#   - returns the visit count
def count_call_model_visits(message: str) -> int:
    # YOUR CODE HERE
    pass


# STEP 3 — call count_call_model_visits once for ONE_TOOL_MESSAGE and once
# for TWO_TOOL_MESSAGE, and print both visit counts side by side for direct
# comparison.
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# ONE_TOOL_MESSAGE should show call_model visited exactly twice: once to
# decide to call get_reservation, once more to turn the result into a final
# answer. TWO_TOOL_MESSAGE should show call_model visited at least three
# times: an initial decision, a decision informed by the first tool's
# result, and a final answer - proving the backward edge actually sends
# control back to the model more than once, not just structurally present
# but never exercised.
#
# Common Pitfalls:
# - Testing only with ONE_TOOL_MESSAGE, which can pass every structural
#   check without ever actually exercising the loop; the two-tool test is
#   the one that proves this is a loop and not a single conditional call in
#   disguise.
# - Counting HumanMessage or ToolMessage instances instead of AIMessage
#   instances - only an AIMessage in the list represents one pass through
#   call_model; the human's original message and each tool's raw result are
#   not, themselves, a decision point.
#
# What this demonstrates:
# A visit count you can point to, printed directly from the agent's own
# message history, is a stronger proof the loop works than "the final
# answer looked reasonable" - the same "inspect an intermediate step, don't
# just trust the final output" discipline this program has used since
# Day 12, applied here to an agent's own decision trace.
