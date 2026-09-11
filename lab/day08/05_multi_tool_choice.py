"""
EXERCISE 05 — Multi-tool agents: making sure the model chooses correctly

CONCEPT
-------
Exercise 01 already showed the model choosing a tool. With only one tool
available, a model either calls the one tool it has or doesn't - there's no
way to choose WRONG. With two tools bound at once, that safety disappears: a
poorly worded docstring, or a guest message that's genuinely ambiguous about
which kind of information it needs, can produce a model confidently calling
the WRONG tool - asking the reservation lookup for something only the
policy documents actually answer, or the reverse.

Nothing about the underlying mechanism is new - `bind_tools([...])` still
works by handing the model each tool's name, its parameter schema, and its
docstring, and the model's decision is still "does the task described in
this docstring match what I need to do right now," now repeated once per
bound tool. Each tool's OWN DOCSTRING is the entire defense against a wrong
choice: a docstring that only says what a tool does, without saying WHEN to
reach for it over an alternative, is the single most common cause of a
multi-tool agent calling the wrong one.

This exercise builds that defense as a genuine test-and-fix loop: write two
CLEARLY-scoped test messages (one that should only need each tool), confirm
which tool actually got called, and if either one is wrong, sharpen that
tool's docstring - not the routing code - and re-test until it resolves
correctly.

RUNNING SCENARIO
-----------------
The same two tools from prior exercises, tested with two deliberately
clearly-scoped messages to confirm the model picks the right one for each,
with the specific tool actually called printed (not just whether the final
answer "looks" reasonable).

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the same two tools and compiled agent shape as prior exercises.
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
from langchain_core.messages import HumanMessage, AIMessage

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
EMBEDDING_MODEL = "text-embedding-3-small"

model = init_chat_model(CHAT_MODEL)

SAMPLE_RESERVATIONS = {
    "214": "check_in=2026-09-20, status=confirmed",
    "310": "check_in=2026-09-25, status=pending",
}

# NOTE: this exercise's whole point is testing and, if needed, REVISING this
# docstring (Step 4 below) - unlike prior exercises, this one is not marked
# "nothing to change here."
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
    collection_name="day08_ex05_hospitality_docs",
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

# Deliberately clearly-scoped, one per tool - each should trigger exactly
# one, unambiguous tool choice.
RESERVATION_TEST_MESSAGE = "What's the check-in date on reservation 310?"
POLICY_TEST_MESSAGE = "Is the spa open on weekends, and until what time?"

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — rebuild the exercise 02-style compiled agent here: AgentState
# (messages only, Annotated[list, add_messages]), call_model, ToolNode(tools)
# named "tools", the conditional edge via tools_condition, and the
# loop-closing edge. Compile into `agent`.
# YOUR CODE HERE


# STEP 2 — write get_first_tool_called(message: str) -> str | None that:
#   - invokes agent with {"messages": [HumanMessage(content=message)]}
#   - scans the final state's messages for the FIRST AIMessage that has
#     tool_calls, and returns that first tool call's "name"
#   - returns None if no message ever had a tool call
def get_first_tool_called(message: str) -> str | None:
    # YOUR CODE HERE
    pass


# STEP 3 — call get_first_tool_called for RESERVATION_TEST_MESSAGE and for
# POLICY_TEST_MESSAGE, printing each message next to the tool name actually
# called, and an explicit PASS/FAIL line comparing it against the tool you
# expected ("get_reservation" and "answer_guest_question" respectively).
# YOUR CODE HERE


# STEP 4 — IF either test in Step 3 prints FAIL: revise that tool's own
# docstring above (in GIVEN) to state more clearly WHEN it should (and
# should NOT) be used relative to the other tool - for example, naming the
# specific kind of question it does NOT answer - then re-run Steps 1-3 and
# confirm both tests now PASS. If both already passed, write one sentence
# here explaining why you believe the current docstrings are unambiguous
# enough that this step wasn't needed.
# YOUR CODE HERE (or your one-sentence note, as a comment)


# EXPECTED RESULT
# ----------------
# Both RESERVATION_TEST_MESSAGE and POLICY_TEST_MESSAGE resolve to the
# correct, single tool call, confirmed by name printed directly from the
# agent's own trace - not inferred from whether the final answer "sounds"
# right.
#
# Common Pitfalls:
# - Judging correctness by reading the final answer's text instead of the
#   actual tool_calls printed - a model can sometimes produce a plausible-
#   sounding answer even after calling the wrong tool, especially if the
#   wrong tool's result happens to overlap with the right one.
# - "Fixing" a wrong choice by rewording the TEST MESSAGE instead of the
#   TOOL'S DOCSTRING - that only hides the problem for this one message; a
#   real guest won't phrase their question to match your test case.
# - Making a docstring longer without making it more DISTINGUISHING - what
#   fixes a wrong choice is narrowing each docstring's stated scope relative
#   to the other tool, not simply adding more words.
