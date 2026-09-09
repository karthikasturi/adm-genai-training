"""
EXERCISE 02 — Chains: composing multi-step LLM calls with LangGraph

CONCEPT
-------
Classifying a guest's message (exercise 01) is only half the job - the
other half is drafting an actual reply. Folding "classify AND respond" into
one prompt is a real trade-off: it does one half well and the other
sloppily, or grows long enough that testing it cleanly (Day 12's discipline)
stops working. A CHAIN is a deliberately authored sequence of steps where
at least one step calls an LLM and a later step's input includes an earlier
step's output - here, a classify step feeding a respond step. LangGraph
gives you the building blocks: a STATE (what data flows between steps), a
NODE (one step, a plain function), and an EDGE (a fixed connection from one
node to the next).

This exercise builds the two-step chain WITHOUT a branch yet (every message
gets the same generic reply template regardless of category) - exercise 03
upgrades this into a real branch.

RUNNING SCENARIO
-----------------
Your capstone's Sprint 3 AI feature: classify a hotel guest's message, then
draft a reply to it.
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

# Reused from exercise 01, unchanged.
CLASSIFY_TEMPLATE_TEXT = (
    "You are a hospitality request classifier.\n"
    "Read the guest's message and respond with exactly one word: "
    "MAINTENANCE, CONCIERGE, or BILLING.\n\n"
    "Guest message: {guest_message}"
)

# One generic reply template for now - every category gets the same
# treatment until exercise 03 gives each category its own template.
REPLY_TEMPLATE_TEXT = (
    "Draft a short, courteous reply to this guest message: {guest_message}"
)

GUEST_MESSAGE = "The AC in room 214 won't turn off."

MODEL = "anthropic:claude-opus-5"  # or "openai:gpt-5.6"


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and model.
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
#   from langchain_core.prompts import PromptTemplate
#   from langchain.chat_models import init_chat_model
#   model = init_chat_model(MODEL)


# STEP 1 — define the state: a TypedDict named RequestState with three
# string fields - guest_message, category, reply. This is what flows from
# node to node; every node reads some of these fields and returns updates
# to others.


# STEP 2 — write classify_node(state: RequestState) -> dict:
#   - build a PromptTemplate from CLASSIFY_TEMPLATE_TEXT (or build it once
#     above the function and reuse it - either works)
#   - format it with state["guest_message"], call model.invoke(...) on the
#     result
#   - print the raw classification (this is "inspecting an intermediate
#     step" - seeing what this ONE step produced before the next step
#     consumes it)
#   - return {"category": <the classification text, stripped and upper-cased>}
#     (a node must return a dict of the state keys it's updating, not the
#     raw model response object)


# STEP 3 — write reply_node(state: RequestState) -> dict:
#   - build a PromptTemplate from REPLY_TEMPLATE_TEXT, format it with
#     state["guest_message"], call model.invoke(...)
#   - return {"reply": <the reply text>}
#   (notice this node ignores state["category"] for now - that's next.)


# STEP 4 — build the graph:
#   builder = StateGraph(RequestState)
#   builder.add_node("classify_node", classify_node)
#   builder.add_node("reply_node", reply_node)
#   builder.add_edge(START, "classify_node")
#   builder.add_edge("classify_node", "reply_node")
#   builder.add_edge("reply_node", END)
#   chain = builder.compile()


# STEP 5 — invoke the compiled chain:
#   chain.invoke({"guest_message": GUEST_MESSAGE, "category": "", "reply": ""})
# Print the classification you saw in Step 2's print, then the final
# state's "reply" value.

# What this demonstrates:
# A chain is state flowing through a fixed sequence of plain functions -
# nothing magic about the "framework" part, just a declared shape instead
# of hand-rolled dictionaries and function calls. Printing inside a node
# (Step 2) is the debugging technique: it shows exactly what one step
# produced before the next step ever runs on it.
