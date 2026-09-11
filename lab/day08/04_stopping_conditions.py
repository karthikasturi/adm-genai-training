"""
EXERCISE 04 — Stopping conditions: task completion vs. a bounded-step failsafe

CONCEPT
-------
Exercise 02's closing note named the gap directly: nothing stops that loop
from continuing forever if the model never stops requesting tool calls. An
ambiguous message, a tool result the model keeps trying to clarify, or a
genuine model error could all produce a model that calls a tool, gets a
result, and immediately decides it needs another tool call, indefinitely.

Two genuinely different kinds of "stop" matter here, and conflating them is
a real risk worth naming plainly:
  - TASK COMPLETION - the loop's own designed, desired ending: the model
    produces a final answer with no further tool calls. `tools_condition`'s
    own "__end__" outcome already detects this - exercise 02's first
    stopping condition, already built.
  - A BOUNDED-STEP LIMIT - a failsafe for when task completion never
    actually arrives: a maximum number of passes through the model node,
    enforced whether or not the model itself believes it's done.

Two mechanisms exist for that second kind, at two different levels:
  - `recursion_limit`, passed once in a graph's run config
    (agent.invoke(..., {"recursion_limit": N})), is a graph-wide safety net
    that counts every super-step the WHOLE graph takes and raises a hard
    GraphRecursionError the moment it's exceeded - a genuinely useful
    backstop, but a blunt one: it ends the run with an unhandled exception,
    not a clean, designed answer.
  - A state-held step_count field, incremented once per pass through
    call_model and checked by the SAME routing function that already checks
    tools_condition, produces a clean, designed stop instead - the agent's
    own final answer can report it ran out of steps, rather than crashing.

Both are worth building: the state-based counter is what this exercise's
routing function implements by hand; recursion_limit stays set underneath
it, at a comfortably higher value, as a safety net against a bug in that
state-based logic itself - belt and suspenders, not either-or.

RUNNING SCENARIO
-----------------
The same agent from exercises 02-03, now with a designed step bound added,
tested two ways: once proving it stops on task completion (not the step
bound) for a normal message, and once proving it stops cleanly at the bound
for a message that would otherwise need more steps than the bound allows.

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the same two tools as prior exercises. Nothing to change here.
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
MAX_STEPS = 5  # a reasonable starting bound for a two-tool task

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
    collection_name="day08_ex04_hospitality_docs",
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

NORMAL_MESSAGE = "Can you check the status of reservation 214 for me?"
# Deliberately open-ended, likely to push the model toward multiple tool
# calls - useful for proving the step bound actually engages.
OPEN_ENDED_MESSAGE = "Tell me everything about my stay - reservation 214, pet policy, checkout, cancellation, spa, and Wi-Fi."

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — define AgentState with TWO fields this time: messages
# (Annotated[list, add_messages], as before) and step_count (int).
# YOUR CODE HERE


# STEP 2 — write call_model(state: AgentState) -> dict that invokes
# model_with_tools on state["messages"], prints the decision (as in prior
# exercises), and returns BOTH updated fields:
#   {"messages": [response], "step_count": state.get("step_count", 0) + 1}
def call_model(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 3 — write route_with_step_limit(state: AgentState) -> str that:
#   - returns "__end__" the moment state["step_count"] >= MAX_STEPS, printing
#     a clear message that the step bound was hit
#   - otherwise returns tools_condition(state) - deferring to the ordinary
#     task-completion check
def route_with_step_limit(state) -> str:
    # YOUR CODE HERE
    pass


# STEP 4 — build the graph: AgentState nodes call_model and a ToolNode(tools)
# named "tools", START -> call_model, a conditional edge from call_model
# using route_with_step_limit (NOT tools_condition directly) mapping "tools"
# to your tool node and "__end__" to END, and the loop-closing edge from the
# tool node back to call_model. Compile into `agent`.
# YOUR CODE HERE


# STEP 5 — TASK-COMPLETION TEST: invoke agent with NORMAL_MESSAGE (initial
# state includes step_count: 0) and a generous recursion_limit (e.g. 50) as
# a safety net in the run config. Confirm from the printed trace that it
# stopped because the model produced a final answer, not because step_count
# reached MAX_STEPS.
# YOUR CODE HERE


# STEP 6 — STEP-BOUND TEST: temporarily lower MAX_STEPS to a very small
# number (for example, reassign MAX_STEPS = 1 right before this call, or
# invoke a second graph compiled with a lower bound) and invoke agent again
# with OPEN_ENDED_MESSAGE. Confirm from the printed trace that it stopped
# cleanly at the bound - the "step bound hit" message from Step 3 - rather
# than raising an unhandled error.
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# NORMAL_MESSAGE stops on task completion, well under MAX_STEPS. With
# MAX_STEPS deliberately set very low, OPEN_ENDED_MESSAGE stops cleanly at
# the bound with your own designed message, instead of looping indefinitely
# or crashing with GraphRecursionError.
#
# Common Pitfalls:
# - Leaving MAX_STEPS at a value so high that Step 6's test never actually
#   exercises the bound - this looks like a passing test but never proves
#   the stopping condition works. Deliberately lowering it for one test run
#   is what actually proves it.
# - Confusing recursion_limit's hard GraphRecursionError with the graceful,
#   state-based stop this exercise is actually about; setting only
#   recursion_limit and skipping the state-based step_count check builds the
#   safety net, not the designed stopping condition.
# - Checking the step bound AFTER calling tools_condition instead of before
#   it - route_with_step_limit must check step_count FIRST, so the bound can
#   override a tool call the model still wants to make.
