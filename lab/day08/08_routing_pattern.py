"""
BONUS EXERCISE 08 — Routing: a hard-coded router vs. a model-based router

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section for why it's included and cited from.

CONCEPT
-------
Anthropic's own "Building Effective Agents" names a clean distinction: a
WORKFLOW is a system where LLMs and tools are orchestrated through
PREDEFINED code paths; an AGENT is a system where the LLM dynamically
directs its own process. Exercises 01-07 built an agent. ROUTING is one of
five named WORKFLOW patterns that sit a level below full agent autonomy -
useful precisely when you want the LLM's judgment for ONE decision (which
specialized path fits this input?) without handing it an open-ended loop.

Day 15's own `route_by_category` (lab/day06/03_branching_chain.py) is
already a router - a "deliberately dumb" one, in that module's own words: a
few lines of Python checking one field. That's exactly right when the
categories are fixed and cheaply distinguishable by keyword or field value.
It stops being right the moment routing itself requires understanding
FREE-TEXT MEANING a keyword check can't reliably catch - the same gap
Module 17A's Topic 1 opened with. A MODEL-BASED router replaces the
hard-coded check with one small, constrained LLM call whose only job is to
output a specialization label, which the surrounding code then uses to pick
a fixed downstream path - still a workflow (the path itself is predefined
and fixed once chosen), not an agent (the LLM never decides how many steps
to take or loops on its own).

RUNNING SCENARIO
-----------------
The same guest-message classification job as Day 15, run two ways side by
side: a hard-coded keyword router, and a model-based router, on messages
deliberately chosen to make the hard-coded version fail.
# [Placeholder — replace with a routing decision from your own Sprint 3
# agent task, e.g. routing a request to a concierge-handling path vs. an
# inventory-handling path]

SETUP
-----
    pip install langchain python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — sample messages, deliberately including one a keyword router
# genuinely cannot classify correctly. Nothing to change here.
# =============================================================================

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

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
    "MAINTENANCE, CONCIERGE, or BILLING. Respond with only the category word.\n\n"
    "Guest message: {guest_message}"
)

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — write keyword_router(message: str) -> str, a DELIBERATELY dumb,
# hard-coded router (Day 15's own style): check for a small, fixed set of
# substrings (for example, "broken" or "not working" -> MAINTENANCE,
# "recommend" or "restaurant" -> CONCIERGE) and return the matching
# category, or "UNKNOWN" if nothing matches. No LLM call in this function.
def keyword_router(message: str) -> str:
    # YOUR CODE HERE
    pass


# STEP 2 — write model_router(message: str) -> str: format
# ROUTING_TEMPLATE_TEXT with the message, call model.invoke(...), and return
# the stripped, upper-cased response text as the category.
def model_router(message: str) -> str:
    # YOUR CODE HERE
    pass


# STEP 3 — run BOTH routers against EASY_MESSAGES and HARD_MESSAGE, printing
# each message next to both routers' outputs side by side, so a disagreement
# is easy to spot at a glance.
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# Both routers should agree on EASY_MESSAGES (or come close). On
# HARD_MESSAGE, keyword_router should return "UNKNOWN" (or a wrong category,
# if one of its substrings happens to false-match) while model_router
# correctly returns "MAINTENANCE" - the concrete, printed proof that routing
# based on MEANING catches cases a fixed keyword check structurally cannot,
# without needing the full decision-loop machinery of exercises 01-07 to get
# there. This is the same trade-off Module 17A Topic 2 named for tool
# choice, one level down: a routing decision, made once, not repeatedly in
# a loop.
#
# What this demonstrates:
# Routing sits BELOW a full agent on Anthropic's own workflow-to-agent
# spectrum: one LLM call decides which of several PREDEFINED paths to take,
# then that path runs on rails - no looping, no repeated tool-choice
# decisions. Reach for this when you have a fixed, small set of downstream
# paths and the only genuinely hard part is classifying the input correctly
# - reach for exercises 01-07's full agent loop when the NUMBER of steps
# itself can't be known in advance.
"""
Sources:
- Anthropic: Building Effective Agents — https://www.anthropic.com/engineering/building-effective-agents
"""
