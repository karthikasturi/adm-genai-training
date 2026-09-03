"""
EXERCISE 03 — Iterative refinement: run -> observe -> revise -> re-run

CONCEPT
-------
Prompt engineering is not "write the perfect prompt once." It's a loop: run
it, look at what came back, notice what's wrong, edit the prompt to fix
that *specific* thing, then run again to confirm the fix held without
breaking what already worked. This exercise walks through one real cycle
against exercise 02's three-example prompt.

RUNNING SCENARIO
-----------------
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

# Exercise 02's three-example standing instruction.
INSTRUCTION = """
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
<example>
Message: "I was charged twice for my subscription this month."
Category: Billing
Confidence: 0.97
Reason: A duplicate charge is a billing dispute, not a technical fault.
</example>

<example>
Message: "The app crashes every time I try to upload a photo."
Category: Technical
Confidence: 0.95
Reason: A reproducible crash is a product defect, not an account or payment issue.
</example>

<example>
Message: "My payment went through but the service still says it's disabled."
Category: Technical
Confidence: 0.6
Reason: The payment itself succeeded; the unresolved problem is that access
wasn't enabled, which the technical team, not billing, needs to fix.
</example>

# Context
This assistant only classifies messages - it never drafts replies, issues
refunds, or takes any other action.
""".strip()

# The original test message from exercise 02, kept in the mix so we can
# confirm a later revision doesn't break what already worked.
ORIGINAL_MESSAGE = "I paid for the premium plan but I still can't access the premium features."

# A new message, similar in shape but worded differently, that tends to get
# classified inconsistently by INSTRUCTION: it mentions a billing event
# (wrong renewal price) AND a technical symptom (features locked) in the
# same sentence.
# [Placeholder — replace with real data]
NEW_MESSAGE = "My subscription renewed at the wrong price and now the premium features are locked."

# The fix, decided after observing NEW_MESSAGE's inconsistent results below
# (this is the "revise" step - normally YOU write this by hand after
# reading the failure; it's given here so the exercise has a concrete
# before/after to run).
REVISION = """

# Refinement
If a message mentions BOTH a payment/subscription problem AND a product
feature not working, classify it by which team can actually fix the root
cause - not by which topic is mentioned first in the sentence."""


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and client. Same as exercise 01:
#   OpenAI    : from openai import OpenAI; client = OpenAI()
#   Anthropic : import anthropic; client = anthropic.Anthropic()


# STEP 1 — run: call the model with INSTRUCTION against NEW_MESSAGE THREE
# separate times, then once more against ORIGINAL_MESSAGE as a control.
# Print each (message, output) pair as you go.
#   OpenAI    : client.responses.create(model="gpt-5.6",
#                 input=[{"role": "developer", "content": INSTRUCTION},
#                        {"role": "user", "content": <message>}])
#               -> response.output_text
#   Anthropic : client.messages.create(model="claude-opus-5", max_tokens=300,
#                 system=INSTRUCTION,
#                 messages=[{"role": "user", "content": <message>}])
#               -> next(b.text for b in response.content if b.type == "text")
#                  (claude-opus-5 thinks by default - filter by type,
#                  don't index response.content[0] directly)


# STEP 2 — observe: look at the three NEW_MESSAGE outputs from Step 1. Do
# they agree with each other? Do they land on the team that can actually
# fix the problem (Technical - locked features), or drift toward Billing
# because the sentence mentions a renewal price first? Write down (as a
# comment or a print statement) what you noticed.


# STEP 3 — revise: build REVISED_INSTRUCTION by appending REVISION to
# INSTRUCTION (simple string concatenation). Print it so you can see the
# final prompt.


# STEP 4 — re-run: repeat Step 1 exactly, but with REVISED_INSTRUCTION
# instead of INSTRUCTION - three calls on NEW_MESSAGE, one on
# ORIGINAL_MESSAGE. Print each (message, output) pair.


# STEP 5 — confirm: compare Step 4's outputs to Step 1's. NEW_MESSAGE
# should now classify the same way every run; ORIGINAL_MESSAGE should
# still be correct. If either isn't true, the fix isn't done - that's a
# normal outcome of one iteration, not a bug in this exercise.

# What this demonstrates:
# Iterative refinement is a loop you drive by hand, not a one-shot write.
# Running the same message multiple times surfaces inconsistency that a
# single run would hide; a fix aimed at that specific failure only counts
# once you've re-run it against BOTH the failing case and the cases that
# already worked.
