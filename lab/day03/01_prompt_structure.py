"""
EXERCISE 01 — Prompt structure: standing instructions vs. the request

CONCEPT
-------
Both OpenAI and Anthropic let you send "standing instructions" (rules that
hold for every request) separately from the "user message" (the one
specific thing you're asking right now). This exercise sends the SAME
information two ways - crammed into one string, then properly split - so
you can see why the split matters once instructions get bigger.

RUNNING SCENARIO (used across this whole exercise set)
--------------------------------------------------------
Classify an inbound customer support message into Billing, Technical, or
General, with a confidence score (0-1) and a one-sentence reason.
# [Placeholder — replace with your own task]

SETUP
-----
    pip install openai anthropic python-dotenv
    export OPENAI_API_KEY=...      # and/or
    export ANTHROPIC_API_KEY=...
"""

# =============================================================================
# GIVEN — the prompt content for this exercise. Nothing to change here.
# =============================================================================

# Everything mixed into one string: category rules + the customer message,
# with no separation between "standing rule" and "this one request."
BAD_PROMPT = (
    "You're a support triage bot. Categories: Billing (payment, charges, "
    "refunds, invoices, subscription cost), Technical (bugs, crashes, "
    "errors, features not working), General (anything else). Give the "
    "category, a confidence score 0-1, and a one-sentence reason. Here's "
    "the message: \"I was charged twice for my subscription this month.\""
)

# The same rules, structured as a standing instruction with four labeled
# sections - Identity, Instructions, Examples, Context. Examples is empty
# for now (that's exercise 02's job).
STANDING_INSTRUCTION = """
# Identity
You are a support-ticket triage assistant for a software product.
# [Placeholder — replace with your own task]

# Instructions
Classify the customer's message into exactly one of three categories:
- Billing: payments, charges, refunds, invoices, subscription cost.
- Technical: bugs, crashes, errors, features not working as expected.
- General: anything else, including account questions or feedback.
Respond with the category, a confidence score between 0 and 1, and a
one-sentence reason that names the specific fact that drove the decision.

# Examples
(none yet)

# Context
This assistant only classifies messages - it never drafts replies, issues
refunds, or takes any other action.
""".strip()

# The one-off request, sent separately from STANDING_INSTRUCTION in the
# "good" version.
USER_MESSAGE = "I was charged twice for my subscription this month."


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it. Nothing here runs until you fill it in.
# =============================================================================

# STEP 0 — imports and client.
#   - Import the SDK for whichever provider you're using:
#       OpenAI    : from openai import OpenAI
#       Anthropic : import anthropic
#   - Create the client (it reads your API key from the environment):
#       OpenAI    : client = OpenAI()
#       Anthropic : client = anthropic.Anthropic()


# STEP 1 — send BAD_PROMPT as a single user turn, no system/developer
# message at all.
#   - OpenAI:
#       response = client.responses.create(
#           model="gpt-5.6",
#           input=[{"role": "user", "content": BAD_PROMPT}],
#       )
#       print(response.output_text)
#   - Anthropic:
#       response = client.messages.create(
#           model="claude-opus-5",
#           max_tokens=300,
#           messages=[{"role": "user", "content": BAD_PROMPT}],
#       )
#       print(next(b.text for b in response.content if b.type == "text"))
#       (claude-opus-5 thinks by default, so response.content can start
#       with a "thinking" block before the "text" block with your answer -
#       filter by type instead of indexing response.content[0] directly.)


# STEP 2 — send STANDING_INSTRUCTION as the standing instruction and
# USER_MESSAGE as the separate request.
#   - OpenAI: same call as Step 1, but input= becomes a two-item list -
#       [{"role": "developer", "content": STANDING_INSTRUCTION},
#        {"role": "user", "content": USER_MESSAGE}]
#   - Anthropic: same call as Step 1, but add a top-level
#       system=STANDING_INSTRUCTION parameter, and messages= carries only
#       USER_MESSAGE.
#   - Print the output text the same way as Step 1.


# STEP 3 — compare.
#   - Print both outputs (Step 1's and Step 2's) one after another.
#   - Look at: did the category/confidence/reason change? Is either
#     output harder to trust, or harder to parse, than the other?

# What this demonstrates:
# Mixing standing rules and the one-off request into a single string works
# often enough to feel fine - until the rules grow (examples, guardrails,
# format requirements) and there's no clean place to put the new piece.
# Splitting them from the start keeps each part independently editable.
