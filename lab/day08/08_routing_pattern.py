"""
BONUS EXERCISE 08 — Routing: a hard-coded router vs. a graph-based router

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section for why it's included and cited from.

CONCEPT
-------
Exercises 01-07 built an AGENT: the model itself decides, repeatedly, which
tool to call next, inside a loop with a backward-pointing edge. ROUTING is a
smaller, more constrained shape - LangGraph's own documented "Routing"
workflow pattern - useful precisely when you want the model's judgment for
ONE decision (which of several fixed, predefined paths fits this input?)
without handing it an open-ended loop. Confirmed directly against LangGraph's
own current documentation ("Workflows and agents"), a routing graph has three
pieces: a node that calls a model with structured output to classify the
input, a plain Python function that reads that classification and returns
the name of the next node, and `add_conditional_edges` wiring that function
to the graph so the runtime dispatches to whichever destination node the
classification named - "the graph routes based on model output," not on
anything the model directly controls about the graph's shape. That's the
same "workflow vs. agent" line Module 17A's own content draws: the model
supplies ONE judgment, the graph's own predefined edges decide what happens
with it - unlike exercises 01-07's loop, where the model itself repeatedly
decides how many steps to take.

Day 15's own `route_by_category` (lab/day06/03_branching_chain.py) is
already a router - a "deliberately dumb" one, in that module's own words: a
few lines of Python checking one field. That's exactly right when the
categories are fixed and cheaply distinguishable by keyword or field value.
It stops being right the moment routing itself requires understanding
FREE-TEXT MEANING a keyword check can't reliably catch - the same gap
Module 17A's Topic 1 opened with. This exercise keeps that hard-coded
router for contrast, then builds the model-based alternative as an actual
LangGraph graph - not just a function that returns a label, but one that
also dispatches to a real downstream node per category, the same
"classify, then act on a predefined path" shape a production router needs.

RUNNING SCENARIO
-----------------
The same guest-message classification job as Day 15, run two ways side by
side: a hard-coded keyword router, and a LangGraph routing graph, on
messages deliberately chosen to make the hard-coded version fail.
# [Placeholder — replace with a routing decision from your own Sprint 3
# agent task, e.g. routing a request to a concierge-handling path vs. an
# inventory-handling path]

SETUP
-----
    pip install langchain langgraph pydantic python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — sample messages, deliberately including one a keyword router
# genuinely cannot classify correctly. Nothing to change here.
# =============================================================================

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Literal

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
model = init_chat_model(CHAT_MODEL)

CATEGORIES = ["MAINTENANCE", "CONCIERGE", "BILLING"]

# Easy for a keyword router: the category word (or an obvious synonym)
# actually appears in the message.
EASY_MESSAGES = [
    "The air conditioning is broken in my room.",       # "broken" -> MAINTENANCE-ish keyword
    "Can you recommend a good restaurant nearby?",        # "recommend" -> CONCIERGE-ish keyword
]

# Deliberately hard for a keyword router: genuine meaning, no matching
# keyword at all.
HARD_MESSAGE = "There's a weird buzzing sound coming from the wall outlet."  # MAINTENANCE, no obvious keyword

ROUTING_TEMPLATE_TEXT = (
    "Classify this hotel guest message into exactly one category: "
    "MAINTENANCE, CONCIERGE, or BILLING.\n\nGuest message: {guest_message}"
)

class Route(BaseModel):
    category: Literal["MAINTENANCE", "CONCIERGE", "BILLING"] = Field(
        description="The single category that best fits the guest's message"
    )

router_model = model.with_structured_output(Route)

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 0 — additional imports you'll need beyond GIVEN's:
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
# YOUR CODE HERE


# STEP 1 — write keyword_router(message: str) -> str, a DELIBERATELY dumb,
# hard-coded router (Day 15's own style): check for a small, fixed set of
# substrings (for example, "broken" or "not working" -> MAINTENANCE,
# "recommend" or "restaurant" -> CONCIERGE) and return the matching
# category, or "UNKNOWN" if nothing matches. No LLM call, no graph, in this
# function - it exists purely as this exercise's contrast case.
def keyword_router(message: str) -> str:
    # YOUR CODE HERE
    pass


# STEP 2 — define RouterState, a TypedDict with three fields: message (str),
# category (str), and response (str).
# YOUR CODE HERE


# STEP 3 — write classify(state: RouterState) -> dict:
#   - format ROUTING_TEMPLATE_TEXT with state["message"]
#   - call router_model.invoke(...) to get a Route object
#   - return {"category": result.category}
def classify(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 4 — write three destination node functions, one per category, each
# returning a dict with one key, "response", holding a short string that
# names the category and echoes the original message - for example
# handle_maintenance should return
# {"response": f"[MAINTENANCE] Logging a maintenance ticket for: {state['message']}"}.
# Write handle_maintenance, handle_concierge, and handle_billing this way.
def handle_maintenance(state) -> dict:
    # YOUR CODE HERE
    pass

def handle_concierge(state) -> dict:
    # YOUR CODE HERE
    pass

def handle_billing(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 5 — write route_decision(state: RouterState) -> str, the plain
# Python function `add_conditional_edges` will call: read state["category"]
# and return one of "maintenance", "concierge", or "billing" (lowercase -
# these are the destination NODE NAMES you'll register in Step 6, not the
# category strings themselves).
def route_decision(state) -> str:
    # YOUR CODE HERE
    pass


# STEP 6 — build the graph:
#   - builder = StateGraph(RouterState)
#   - add classify, handle_maintenance, handle_concierge, and
#     handle_billing as nodes, naming them "classify", "maintenance",
#     "concierge", and "billing" respectively
#   - connect START to "classify"
#   - add a conditional edge from "classify" using route_decision, mapping
#     "maintenance" -> "maintenance", "concierge" -> "concierge",
#     "billing" -> "billing"
#   - add a plain edge from each of the three destination nodes to END
#   - compile the graph into `router_graph`
# YOUR CODE HERE


# STEP 7 — run BOTH keyword_router and router_graph against EASY_MESSAGES
# and HARD_MESSAGE. For the graph, invoke it with
# {"message": message} as the initial state and read the final state's
# "category" and "response". Print each message next to both routers'
# category output side by side, so a disagreement is easy to spot at a
# glance.
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# Both routers should agree on EASY_MESSAGES (or come close). On
# HARD_MESSAGE, keyword_router should return "UNKNOWN" (or a wrong category,
# if one of its substrings happens to false-match) while router_graph
# correctly classifies it MAINTENANCE and its final state's "response"
# shows the maintenance-handling node actually ran - concrete, printed
# proof that routing on MEANING catches cases a fixed keyword check
# structurally cannot, and that the classification actually drove which
# downstream node executed, not just which label got printed.
#
# What this demonstrates:
# Routing sits BELOW a full agent on the workflow-to-agent spectrum: one
# structured-output model call decides which of several PREDEFINED graph
# paths to take, then that path runs on rails - no looping, no repeated
# tool-choice decisions, no edge the model itself controls. Reach for this
# when you have a fixed, small set of downstream paths and the only
# genuinely hard part is classifying the input correctly - reach for
# exercises 01-07's full agent loop when the NUMBER of steps itself can't
# be known in advance.
#
# Common Pitfalls:
# - Returning the raw category string ("MAINTENANCE") from route_decision
#   instead of the lowercase NODE NAME ("maintenance") registered in
#   add_conditional_edges's mapping - the graph raises an error because it
#   can't find a destination matching what route_decision returned.
# - Forgetting the plain edge from each destination node to END, which
#   leaves the graph technically compiled but with no defined stopping
#   point once a destination node finishes.
# - Building `router_model` fresh inside classify() on every call instead
#   of reusing the module-level one from GIVEN - wasteful, and easy to get
#   the schema binding wrong a second time.
"""
Sources:
- LangGraph: Workflows and agents (Routing) — https://docs.langchain.com/oss/python/langgraph/workflows-agents
"""
