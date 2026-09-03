"""
EXERCISE 04 — Score two prompt versions against a fixed test set

CONCEPT
-------
Eyeballing a handful of outputs (like exercises 02 and 03 did) doesn't
scale, and it's easy to fool yourself - a prompt can look better just
because you happened to glance at a favorable example. This exercise
replaces eyeballing with a small, fixed test set and an explicit scoring
rubric, run against two prompt versions, so you get an actual number
instead of a gut feeling.

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
# GIVEN — the prompt content and test data for this exercise. Nothing to
# change here.
# =============================================================================

# Version A: one worked example.
PROMPT_VERSION_A = """
# Identity
You are a support-ticket triage assistant for a software product.
# [Placeholder — replace with your own task]

# Instructions
Classify the customer's message into exactly one of three categories:
- Billing: payments, charges, refunds, invoices, subscription cost.
- Technical: bugs, crashes, errors, features not working as expected.
- General: anything else, including account questions or feedback.
Respond in exactly this format, one line each:
Category: <Billing|Technical|General>
Confidence: <a number between 0 and 1>
Reason: <one sentence naming the specific fact that drove the decision>

# Examples
<example>
Message: "I was charged twice for my subscription this month."
Category: Billing
Confidence: 0.97
Reason: A duplicate charge is a billing dispute, not a technical fault.
</example>

# Context
This assistant only classifies messages - it never drafts replies, issues
refunds, or takes any other action.
""".strip()

# Version B: three worked examples, from exercise 02.
PROMPT_VERSION_B = """
# Identity
You are a support-ticket triage assistant for a software product.
# [Placeholder — replace with your own task]

# Instructions
Classify the customer's message into exactly one of three categories:
- Billing: payments, charges, refunds, invoices, subscription cost.
- Technical: bugs, crashes, errors, features not working as expected.
- General: anything else, including account questions or feedback.
Respond in exactly this format, one line each:
Category: <Billing|Technical|General>
Confidence: <a number between 0 and 1>
Reason: <one sentence naming the specific fact that drove the decision>

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

# 5-message test set: 2 clearly Billing, 2 clearly Technical, 1 ambiguous.
TEST_SET = [
    {"message": "I was charged twice for my subscription this month.", "expected": "Billing", "kind": "clear"},
    # [Placeholder — replace with real data]
    {"message": "Can you send me an itemized invoice for the last three billing cycles?", "expected": "Billing", "kind": "clear"},
    {"message": "The app crashes every time I try to upload a photo.", "expected": "Technical", "kind": "clear"},
    # [Placeholder — replace with real data]
    {"message": "Search results come back empty even for items I can clearly see in my account.", "expected": "Technical", "kind": "clear"},
    {"message": "My payment went through but the service still says it's disabled.", "expected": "Technical", "kind": "ambiguous"},
]

# The scoring rubric - 3 points max per message, 15 max per prompt version:
#   1. Correct category (compare case-insensitively - the model won't
#      always match your exact casing).
#   2. On the ambiguous message ONLY: its confidence should be lower than
#      the confidences you saw on the clear-cut messages. (Clear-cut
#      messages get this point automatically - the rule doesn't apply to
#      them.)
#   3. The reason names the specific distinguishing fact rather than just
#      restating the category ("It's billing." tells you nothing new; "A
#      duplicate charge is a billing dispute" does).


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and client. Same as exercise 01:
#   OpenAI    : from openai import OpenAI; client = OpenAI()
#   Anthropic : import anthropic; client = anthropic.Anthropic()
#   Also import `re` - you'll want it in Step 1 to pull fields out of the
#   plain-text response.


# STEP 1 — write a small parse_response(text) function that takes the
# model's raw text and returns a dict {"category": ..., "confidence": ...,
# "reason": ...}. The response follows "Category: X / Confidence: Y /
# Reason: Z" on separate lines (per the prompts above) - a few
# re.search() calls (or even text.splitlines() + string slicing) is
# enough; it doesn't need to be bulletproof.


# STEP 2 — write a score(expected_category, parsed, clear_confidences)
# function implementing the rubric above. `clear_confidences` is a list of
# confidence scores already collected from the clear-cut messages in this
# same run - pass an empty list when scoring a clear-cut message itself,
# and the real list when scoring the ambiguous one. Return the point total
# (0-3).


# STEP 3 — for PROMPT_VERSION_A: loop over TEST_SET twice - once to call
# the model on every "clear" message and collect (confidence, score) using
# an empty clear_confidences list, then once more for the "ambiguous"
# message using the confidences you just collected. Print each message's
# parsed result and score, then the version's total out of 15.
#   OpenAI    : client.responses.create(model="gpt-5.6",
#                 input=[{"role": "developer", "content": PROMPT_VERSION_A},
#                        {"role": "user", "content": <message>}])
#               -> response.output_text
#   Anthropic : client.messages.create(model="claude-opus-5", max_tokens=300,
#                 system=PROMPT_VERSION_A,
#                 messages=[{"role": "user", "content": <message>}])
#               -> next(b.text for b in response.content if b.type == "text")
#                  (claude-opus-5 thinks by default - filter by type,
#                  don't index response.content[0] directly)


# STEP 4 — repeat Step 3 for PROMPT_VERSION_B.


# STEP 5 — print a small score table (version name + total out of 15) and
# say which version won.

# What this demonstrates:
# A fixed test set plus an explicit, points-based rubric turns "does this
# prompt seem better?" into a number you can compare run to run and
# version to version. The rubric itself encodes real quality signals - not
# just "did it get the label right," but "is the confidence honest" and
# "is the reason actually informative" - which is what keeps the score
# from being gameable.
