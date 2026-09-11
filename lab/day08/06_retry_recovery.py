"""
EXERCISE 06 — Retrying and recovering from a failed tool call

CONCEPT
-------
Every tool call built across Days 15-16, and every exercise so far today,
has quietly assumed a tool call either works or raises an error a person
happens to be watching the terminal to notice. Today's agent runs in a loop
specifically designed to keep going without a person watching every single
step - which means a single transient failure (a dropped connection, a
rate-limited request) can no longer be something the code simply doesn't
handle.

Confirmed directly against LangGraph's own ToolNode reference documentation,
this is NOT automatically covered by the tool-execution primitive exercise
02's loop already uses: a bare ToolNode's default `handle_tool_errors`
behavior catches only invalid-argument errors and lets a tool's own real
EXECUTION errors propagate - the opposite of what's needed here, which is a
real execution failure caught and retried, not raised straight past the
loop.

This exercise builds a small, deliberately literal retry wrapper: call the
tool, catch an exception if one is raised, call the EXACT SAME tool with the
EXACT SAME arguments one more time, and only if that second attempt also
fails, give up and return a clear failure message the model can read and
react to - rather than crashing the whole agent. (LangChain's current
middleware stack ships a configurable, production-grade version of this
same idea as ToolRetryMiddleware, worth knowing about but not what's built
by hand here - see the README's bonus-patterns note.)

RUNNING SCENARIO
-----------------
One of today's tools, deliberately modified to fail on its first call and
succeed on its second - a controlled way to simulate a real transient
failure - run through a retry-wrapped tool-execution step, proving both the
"recovers on retry" path and the "gives up cleanly after two failures" path.

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the same two tools as prior exercises, PLUS a deliberately-flaky
# throwaway third tool for this exercise's own testing purposes.
# =============================================================================

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

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
    collection_name="day08_ex06_hospitality_docs",
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

# A deliberately-flaky throwaway tool: fails on its first call, succeeds on
# its second - a controlled stand-in for a real transient failure.
_flaky_call_count = {"n": 0}

@tool
def check_room_availability(room_type: str) -> str:
    """Check live availability for a room type. Simulates a flaky real API call.

    Use this when a guest asks whether a specific room type is available.
    """
    _flaky_call_count["n"] += 1
    if _flaky_call_count["n"] == 1:
        raise ConnectionError("simulated transient failure - availability service timed out")
    return f"{room_type}: 3 rooms available"

# A second, ALWAYS-failing variant, for proving the "give up" path in Step 4.
@tool
def check_room_availability_always_fails(room_type: str) -> str:
    """Check live availability for a room type. Always fails, for testing the give-up path.

    Use this only in exercise 06's own give-up test.
    """
    raise ConnectionError("simulated permanent failure - availability service is down")

tools = [get_reservation, answer_guest_question, check_room_availability]
model_with_tools = model.bind_tools(tools)

FLAKY_TOOL_MESSAGE = "Is a Deluxe King room available?"

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — write call_tool_with_retry(tool, tool_call: dict, max_attempts: int
# = 2) -> str that:
#   - loops from attempt 1 to max_attempts
#   - inside the loop, tries tool.invoke(tool_call["args"]) and returns the
#     result immediately if it succeeds
#   - on an exception, prints which attempt failed and why, and keeps the
#     exception so it can be reported if every attempt fails
#   - after the loop, if every attempt failed, returns a clear string
#     message naming the tool, the attempt count, and the last error
def call_tool_with_retry(tool, tool_call, max_attempts: int = 2) -> str:
    # YOUR CODE HERE
    pass


# STEP 2 — write a tool-execution node, tool_node_with_retry(state) -> dict,
# that replaces the prebuilt ToolNode for this exercise: for each tool call
# in the last message's tool_calls, look up the matching tool object from
# `tools` by name, call call_tool_with_retry(tool, tool_call), and wrap each
# result in a ToolMessage(content=..., tool_call_id=tool_call["id"]).
# Return {"messages": <the list of ToolMessages>}.
def tool_node_with_retry(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 3 — build the graph using tool_node_with_retry in place of a
# prebuilt ToolNode: AgentState (messages only), call_model (as in prior
# exercises), your own tool_node_with_retry as the "tools" node, the
# conditional edge via tools_condition, and the loop-closing edge. Compile
# into `agent`. Invoke it with FLAKY_TOOL_MESSAGE and confirm, from your
# Step 1 printed output, that the first attempt fails and the second
# succeeds, with the loop continuing normally to a final answer.
# YOUR CODE HERE


# STEP 4 — GIVE-UP TEST: build a second, throwaway single-tool setup bound
# only to check_room_availability_always_fails (its own model_with_tools,
# its own tiny graph reusing tool_node_with_retry), invoke it with a message
# that would trigger that tool, and confirm your agent returns the designed
# failure message from Step 1 (naming the retry limit was reached) instead
# of raising an unhandled exception.
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# FLAKY_TOOL_MESSAGE: attempt 1 fails (printed), attempt 2 succeeds
# (printed), and the loop continues to a normal final answer - the retry
# was invisible to the model except for a slightly later result. The
# give-up test: two failed attempts (printed), then a clean failure message
# returned as the tool's result, NOT an unhandled exception - the model gets
# to see the failure and, if bound tools allow it, could still choose to
# answer based on other information rather than the whole agent crashing.
#
# Common Pitfalls:
# - Writing an UNBOUNDED retry (a while True instead of a fixed
#   max_attempts), which silently reintroduces the exact indefinite-loop
#   risk exercise 04's stopping-condition work exists to prevent, just
#   relocated inside a single tool call instead of the outer agent loop.
# - Forgetting to set tool_call_id on each ToolMessage - LangChain matches a
#   tool's result back to its originating request by this ID; a missing or
#   wrong ID breaks that matching even if the retry logic itself is correct.
# - Testing only the "succeeds on retry" path and never actually forcing
#   the "give up after all attempts fail" path (Step 4) - both are real
#   behaviors this exercise is about, not just the happy path.
