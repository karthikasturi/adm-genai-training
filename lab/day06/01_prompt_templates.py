"""
EXERCISE 01 — PromptTemplate: parameterized, reusable prompts

CONCEPT
-------
By Day 12 you already know how to get one well-shaped answer out of a
model with a carefully worded, tested prompt. Retyping that same wording
by hand every time a new input needs it - or worse, retyping it with a
small unintentional wording drift - doesn't scale once a real feature
sends it hundreds of different messages. A PromptTemplate stores a
prompt's fixed wording ONCE, with a named variable slot written directly
into it, so formatting it with a specific input produces the final prompt
without the template's own tested wording ever being edited again.

RUNNING SCENARIO (used across this whole exercise set)
--------------------------------------------------------
Your capstone's Sprint 3 AI feature: a hotel guest sends a free-text
message, and your chain needs to classify what KIND of request it is
before responding to it appropriately.
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

# The classify prompt's fixed wording, with ONE variable slot:
# {guest_message}. This is the exact prompt you'd otherwise have to
# hand-edit for every new guest message.
CLASSIFY_TEMPLATE_TEXT = (
    "You are a hospitality request classifier.\n"
    "Read the guest's message and respond with exactly one word: "
    "MAINTENANCE, CONCIERGE, or BILLING.\n\n"
    "Guest message: {guest_message}"
)

# Two different guest messages - the same template gets reused across both,
# unedited, which is the whole point of a template.
GUEST_MESSAGE_1 = "The AC in room 214 won't turn off."
GUEST_MESSAGE_2 = "Can you recommend a good restaurant nearby?"

# One model string works for either provider - init_chat_model reads the
# prefix before the colon to decide which vendor to call.
MODEL = "anthropic:claude-opus-5"  # or "openai:gpt-5.6"


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and model.
#   from langchain_core.prompts import PromptTemplate
#   from langchain.chat_models import init_chat_model
#   model = init_chat_model(MODEL)
#   (init_chat_model reads your API key from the environment automatically,
#   based on the provider prefix in MODEL - no separate client object.)


# STEP 1 — build the template: classify_template =
# PromptTemplate.from_template(CLASSIFY_TEMPLATE_TEXT).


# STEP 2 — format it for GUEST_MESSAGE_1: call
# classify_template.invoke({"guest_message": GUEST_MESSAGE_1}) and print the
# result. (It's a PromptValue object - print(result.to_string()) or just
# print(result) to see the filled-in prompt text.)


# STEP 3 — format the SAME classify_template again, this time for
# GUEST_MESSAGE_2. Print it too. Compare the two printed prompts by eye -
# only the guest message text should differ; the wording around it is
# identical because it's the same template object both times.


# STEP 4 — actually classify both messages: call model.invoke(...) with
# each of the two PromptValues from Steps 2-3, and print result.content
# for each. You should see one classification per message.

# What this demonstrates:
# A template separates "wording that stays the same" from "the one value
# that changes per call." Reusing classify_template across two different
# guest messages, instead of writing two near-identical prompt strings by
# hand, is what "parameterized and reusable" means in practice - and it's
# the same tested wording every time, with no risk of drift.
