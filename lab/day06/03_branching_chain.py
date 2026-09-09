"""
EXERCISE 03 — Branching: routing to a different node based on state

CONCEPT
-------
Exercise 02's chain always drafts the same generic reply no matter what the
message was classified as - which defeats the point of classifying it in
the first place. A CONDITIONAL EDGE fixes that: instead of a fixed next
node, it takes a routing function that inspects the current state and
returns the NAME of whichever next node should actually run. This is the
outline's own "branch to the chain that routes to a different prompt
template based on the input."

RUNNING SCENARIO
-----------------
Your capstone's Sprint 3 AI feature: classify a hotel guest's message, then
route it to a category-specific reply.
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

# Two category-specific templates now, instead of exercise 02's one
# generic one. (BILLING isn't wired to its own node below -
# # [Placeholder — add a third branch and template if your team's Sprint 3
# feature needs a BILLING path too]. For now, route_by_category treats
# anything that isn't MAINTENANCE as CONCIERGE.)
MAINTENANCE_TEMPLATE_TEXT = (
    "Draft a short, courteous reply logging this maintenance issue: {guest_message}"
)
CONCIERGE_TEMPLATE_TEXT = (
    "Draft a short, courteous concierge reply to this guest request: {guest_message}"
)

# One message per category, so you can confirm each one takes the right branch.
MAINTENANCE_MESSAGE = "The AC in room 214 won't turn off."
CONCIERGE_MESSAGE = "Can you recommend a good restaurant nearby?"

MODEL = "anthropic:claude-opus-5"  # or "openai:gpt-5.6"


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and model. Same as exercise 02:
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
#   from langchain_core.prompts import PromptTemplate
#   from langchain.chat_models import init_chat_model
#   model = init_chat_model(MODEL)


# STEP 1 — define RequestState, same shape as exercise 02: guest_message,
# category, reply (all str).


# STEP 2 — write classify_node(state) -> dict, same as exercise 02's:
# format CLASSIFY_TEMPLATE_TEXT with state["guest_message"], call
# model.invoke(...), print the raw classification, return
# {"category": <stripped, upper-cased text>}.


# STEP 3 — write the routing function:
#   def route_by_category(state: RequestState) -> str:
#       return "maintenance_node" if state["category"] == "MAINTENANCE" else "concierge_node"
# (the string it returns must exactly match a node name you register in
# Step 5 - a mismatch fails at compile or run time, not silently.)


# STEP 4 — write maintenance_node(state) and concierge_node(state), each
# formatting its own template (MAINTENANCE_TEMPLATE_TEXT /
# CONCIERGE_TEMPLATE_TEXT) with state["guest_message"], calling
# model.invoke(...), and returning {"reply": <the reply text>}.


# STEP 5 — build the graph:
#   builder = StateGraph(RequestState)
#   builder.add_node("classify_node", classify_node)
#   builder.add_node("maintenance_node", maintenance_node)
#   builder.add_node("concierge_node", concierge_node)
#   builder.add_edge(START, "classify_node")
#   builder.add_conditional_edges("classify_node", route_by_category,
#                                  ["maintenance_node", "concierge_node"])
#   builder.add_edge("maintenance_node", END)
#   builder.add_edge("concierge_node", END)
#   chain = builder.compile()


# STEP 6 — invoke the chain TWICE: once with MAINTENANCE_MESSAGE, once with
# CONCIERGE_MESSAGE (each time passing {"guest_message": ..., "category":
# "", "reply": ""}). For each call, print the message, the classification
# you saw printed in Step 2, and the final reply - confirming each message
# reached the reply node that actually matches its category.

# What this demonstrates:
# A conditional edge lets the SAME chain send different messages down
# different paths, each with its own tested template, instead of one
# generic node trying to handle every case. Combined with exercise 02's
# print-based inspection, you can now see exactly which category a message
# got AND which node actually ran because of it.
