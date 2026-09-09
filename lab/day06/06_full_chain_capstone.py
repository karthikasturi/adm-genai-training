"""
EXERCISE 06 — Capstone: branch + memory + tool call, one chain

CONCEPT
-------
This exercise combines exercises 03, 04, and 05 into the single shape the
outline itself ends the day on: "classify, branch, remember, call one
tool." Nothing new to learn here - it's the same four mechanisms you
already built separately, wired into one graph:
  - classify_node + a conditional edge routes to a category-specific node
    (exercise 03)
  - a checkpointer + thread_id gives the whole graph memory across
    separate calls (exercise 04)
  - the maintenance path can call a real tool and verify it fired
    correctly (exercise 05)

Only the MAINTENANCE path calls the reservation tool here - not every
branch needs one. This is also explicitly a stopping point, not a loop:
the tool node ends the turn rather than looping back into the model to
draft one more reply from the tool's result - see exercise 05's note on
why an open-ended "call tools until done" loop is a different, later
topic.

RUNNING SCENARIO
-----------------
Your capstone's Sprint 3 AI feature, as a finished skeleton: classify a
guest's message, branch to a category-specific handler, remember the
conversation across turns, and let the maintenance path check a real
reservation.
# [Placeholder — replace with your team's actual Sprint 3 AI feature]

SETUP
-----
    pip install langchain langgraph langchain-anthropic langchain-openai python-dotenv
    export ANTHROPIC_API_KEY=...      # and/or
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the prompt content and sample data for this exercise. Nothing to
# change here.
# =============================================================================

CLASSIFY_TEMPLATE_TEXT = (
    "You are a hospitality request classifier.\n"
    "Read the guest's message and respond with exactly one word: "
    "MAINTENANCE, CONCIERGE, or BILLING.\n\n"
    "Guest message: {guest_message}"
)

# Stand-in for a real reservations database / API - same as exercise 05.
# [Placeholder — replace with a real call to the capstone's own
# GET /api/v1/reservations/{id} endpoint]
SAMPLE_RESERVATIONS = {
    "214": "check_in=2026-09-20, status=confirmed",
    "310": "check_in=2026-09-25, status=pending",
}
RESERVATION_TOOL_DOCSTRING = (
    "Look up a reservation by ID and return its check-in date and status.\n\n"
    "    Use this when a guest's request depends on the details of a "
    "specific, existing reservation rather than a general policy question."
)

FIRST_MESSAGE = "Room 214 AC still isn't working, can you check my reservation status?"
FOLLOWUP_MESSAGE = "Thanks - can someone come by this afternoon?"

THREAD_ID = "guest-214"

MODEL = "anthropic:claude-opus-5"  # or "openai:gpt-5.6"


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and model. Everything from exercises 01-05, combined:
#   from typing import Annotated
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
#   from langgraph.graph.message import add_messages
#   from langgraph.checkpoint.memory import InMemorySaver
#   from langgraph.prebuilt import ToolNode
#   from langchain.tools import tool
#   from langchain_core.prompts import PromptTemplate
#   from langchain_core.messages import HumanMessage
#   from langchain.chat_models import init_chat_model
#   model = init_chat_model(MODEL)


# STEP 1 — define the state: a TypedDict named CapstoneState with two
# fields - messages (Annotated[list, add_messages], exercise 04's pattern)
# and category (a plain str, exercise 03's pattern - recomputed fresh each
# turn, not accumulated).


# STEP 2 — write the tool function, same as exercise 05:
#   @tool
#   def get_reservation(reservation_id: str) -> str:
#       """<RESERVATION_TOOL_DOCSTRING's text>"""
#       return SAMPLE_RESERVATIONS.get(reservation_id, "no reservation found with that ID")


# STEP 3 — write classify_node(state: CapstoneState) -> dict:
#   - read the NEWEST message: state["messages"][-1].content
#   - format CLASSIFY_TEMPLATE_TEXT with it, call the plain model.invoke(...)
#     (no tools bound here - classification doesn't need one)
#   - print the raw classification
#   - return {"category": <stripped, upper-cased text>}


# STEP 4 — write route_by_category(state) -> str, same rule as exercise 03:
# "maintenance_node" if state["category"] == "MAINTENANCE" else "concierge_node".


# STEP 5 — write maintenance_node(state: CapstoneState) -> dict:
#   - model_with_tools = model.bind_tools([get_reservation])
#   - call model_with_tools.invoke(state["messages"]) - the FULL message
#     history, not just the latest one, so the model has context from any
#     earlier turns under this thread_id
#   - return {"messages": [result]}


# STEP 6 — write concierge_node(state: CapstoneState) -> dict: call the
# plain model.invoke(state["messages"]) (no tools), return
# {"messages": [result]}.


# STEP 7 — write route_after_maintenance(state) -> str: return "tools" if
# state["messages"][-1].tool_calls else END - only the maintenance path
# can trigger a tool call, so this routing function is only ever wired
# after maintenance_node.


# STEP 8 — build the graph:
#   builder = StateGraph(CapstoneState)
#   builder.add_node("classify_node", classify_node)
#   builder.add_node("maintenance_node", maintenance_node)
#   builder.add_node("concierge_node", concierge_node)
#   builder.add_node("tools", ToolNode([get_reservation]))
#   builder.add_edge(START, "classify_node")
#   builder.add_conditional_edges("classify_node", route_by_category,
#                                  ["maintenance_node", "concierge_node"])
#   builder.add_conditional_edges("maintenance_node", route_after_maintenance,
#                                  ["tools", END])
#   builder.add_edge("tools", END)
#   builder.add_edge("concierge_node", END)
#   chain = builder.compile(checkpointer=InMemorySaver())


# STEP 9 — invoke with FIRST_MESSAGE under THREAD_ID:
#   config = {"configurable": {"thread_id": THREAD_ID}}
#   chain.invoke({"messages": [HumanMessage(content=FIRST_MESSAGE)]}, config)
# Print every message in the result (type + content). Confirm: the
# classification printed in Step 3 was MAINTENANCE, an AIMessage requested
# get_reservation with reservation_id "214", and a ToolMessage carries back
# the looked-up record.


# STEP 10 — invoke AGAIN with FOLLOWUP_MESSAGE, same THREAD_ID and config.
# Print the messages again - the reply should read as aware of the earlier
# AC/reservation conversation (memory), and the message count should have
# grown rather than reset.


# STEP 11 — not code: as a team, compare this chain's shape (classify,
# branch, remember, call one tool) against your actual Sprint 3 brief.
# Write down (as a comment, or out loud) which category names, templates,
# and the one tool above are placeholders that need to become your team's
# real values before extending this chain further.

# What this demonstrates:
# None of exercises 03-05's mechanisms changed to combine them - a
# conditional edge is still a conditional edge, a checkpointer still just
# needs a thread_id, a tool still just needs binding and a ToolNode. This
# is what "a chain" scales to: more nodes and edges declared explicitly,
# each one still a plain, inspectable function, with no hidden control
# flow deciding on its own to add a step or run part of the graph twice.
