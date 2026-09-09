"""
EXERCISE 05 — Tool integration: calling a real function from a chain

CONCEPT
-------
A model only knows what was in its training data and whatever text is
currently in front of it. It can't look up a real guest's actual
reservation - that's real, live, external data no amount of prompting
alone can produce. A TOOL is a plain Python function, decorated with
@tool, that a model can be offered and can choose to call. Two things
matter: type hints on the function's parameters (they define what shape
of arguments the model is allowed to send it) and the docstring (the
model uses it to decide WHEN this tool is the right one to call).

This exercise is deliberately scoped to ONE verified call, not a loop: one
node's model call may request the tool, LangGraph's prebuilt ToolNode
executes it, and the flow ends there so you can confirm the call actually
fired with the right arguments. An open-ended loop where the model decides
on its own, repeatedly, whether to call a tool again is a different,
later topic - not built here.

RUNNING SCENARIO
-----------------
A guest asks about a specific reservation by ID; the chain needs to look
it up for real instead of guessing.
# [Placeholder — replace with a real call to your capstone's own API]

SETUP
-----
    pip install langchain langgraph langchain-anthropic langchain-openai python-dotenv
    export ANTHROPIC_API_KEY=...      # and/or
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the sample data for this exercise. Nothing to change here.
# =============================================================================

# Stand-in for a real reservations database / API.
# [Placeholder — replace with a real call to the capstone's own
# GET /api/v1/reservations/{id} endpoint]
SAMPLE_RESERVATIONS = {
    "214": "check_in=2026-09-20, status=confirmed",
    "310": "check_in=2026-09-25, status=pending",
}

# The docstring your tool function needs (word for word) - this is what the
# model reads to decide whether and when to call it.
RESERVATION_TOOL_DOCSTRING = (
    "Look up a reservation by ID and return its check-in date and status.\n\n"
    "    Use this when a guest's request depends on the details of a "
    "specific, existing reservation rather than a general policy question."
)

GUEST_MESSAGE = "Can you check the status of reservation 214 for me?"

MODEL = "anthropic:claude-opus-5"  # or "openai:gpt-5.6"


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and model.
#   from typing import Annotated
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
#   from langgraph.graph.message import add_messages
#   from langgraph.prebuilt import ToolNode
#   from langchain.tools import tool
#   from langchain_core.messages import HumanMessage
#   from langchain.chat_models import init_chat_model
#   model = init_chat_model(MODEL)


# STEP 1 — write the tool function:
#   @tool
#   def get_reservation(reservation_id: str) -> str:
#       """<paste RESERVATION_TOOL_DOCSTRING's text here as the actual docstring>"""
#       return SAMPLE_RESERVATIONS.get(reservation_id, "no reservation found with that ID")
# (the type hint on reservation_id is mandatory - it's what tells the model
# what shape of argument this tool expects.)


# STEP 2 — bind the tool to the model:
#   model_with_tools = model.bind_tools([get_reservation])
# (the plain `model` from Step 0 is untouched and still usable without
# tools elsewhere - bind_tools returns a new, tool-aware model.)


# STEP 3 — define the state: a TypedDict named ToolCallState with one
# field, messages, typed as Annotated[list, add_messages] (same pattern as
# exercise 04).


# STEP 4 — write assistant_node(state) -> dict: call
# model_with_tools.invoke(state["messages"]), print the result's
# .tool_calls attribute (a list - empty if the model chose not to call
# anything), and return {"messages": [result]}.


# STEP 5 — write route_after_assistant(state) -> str: return "tools" if
# state["messages"][-1].tool_calls else END - the routing function that
# sends the flow to the tool node ONLY when the model actually requested a
# call.


# STEP 6 — build the graph:
#   builder = StateGraph(ToolCallState)
#   builder.add_node("assistant_node", assistant_node)
#   builder.add_node("tools", ToolNode([get_reservation]))
#   builder.add_edge(START, "assistant_node")
#   builder.add_conditional_edges("assistant_node", route_after_assistant, ["tools", END])
#   builder.add_edge("tools", END)
#   chain = builder.compile()
# (this deliberately does NOT route "tools" back to "assistant_node" - see
# the CONCEPT note above on why this stays a single call, not a loop.)


# STEP 7 — invoke the chain with GUEST_MESSAGE:
#   chain.invoke({"messages": [HumanMessage(content=GUEST_MESSAGE)]})
# Print every message in the result's "messages" list along with its type
# (AIMessage vs. ToolMessage) and content - confirm the AIMessage's
# tool_calls named "get_reservation" with reservation_id "214", and that
# the ToolMessage that follows contains the actual looked-up record.

# What this demonstrates:
# Binding a tool doesn't make the model call it - it makes calling it
# POSSIBLE, based on the model reading the docstring and deciding this
# request needs it. ToolNode is what actually runs your real Python
# function with the arguments the model supplied, and hands the result
# back as a message the next step can read - verified here as one bounded,
# testable call, not an open-ended loop.
