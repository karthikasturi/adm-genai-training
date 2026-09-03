"""
EXERCISE 02 — Zero-shot vs. few-shot

CONCEPT
-------
Telling the model the rules (exercise 01's "good" standing instruction) is
often not enough for it to answer *consistently* - run the same request
three times and you can get three subtly different answers, especially on
a message that sits near a category boundary. Showing the model a few
worked examples of the exact input/output shape you want ("few-shot") tends
to tighten that up. This exercise runs the same message three times at each
of three stages - 0 examples, 1 example, 3 examples - so you can actually
see the effect, not just take it on faith.

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

STANDING_INSTRUCTION_ZERO_SHOT = """
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

STANDING_INSTRUCTION_ONE_SHOT = """
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

# Context
This assistant only classifies messages - it never drafts replies, issues
refunds, or takes any other action.
""".strip()

# Three worked examples, including one deliberately ambiguous case with an
# honestly-lower confidence score (0.6, not 0.95) instead of forcing false
# certainty.
STANDING_INSTRUCTION_FEW_SHOT = """
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

# The message we test at every stage. It's thematically close to the
# ambiguous worked example - payment succeeded, but access is the actual
# unresolved problem - so it's a good candidate for showing whether
# examples stabilize the model's answer.
# [Placeholder — replace with real data]
TEST_MESSAGE = "I paid for the premium plan but I still can't access the premium features."


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and client. Same as exercise 01:
#   OpenAI    : from openai import OpenAI; client = OpenAI()
#   Anthropic : import anthropic; client = anthropic.Anthropic()


# STEP 1 — zero-shot: call the model with STANDING_INSTRUCTION_ZERO_SHOT and
# TEST_MESSAGE, THREE separate times (use a loop). Print each of the three
# raw outputs.
#   OpenAI    : client.responses.create(model="gpt-5.6",
#                 input=[{"role": "developer", "content": STANDING_INSTRUCTION_ZERO_SHOT},
#                        {"role": "user", "content": TEST_MESSAGE}])
#               -> response.output_text
#   Anthropic : client.messages.create(model="claude-opus-5", max_tokens=300,
#                 system=STANDING_INSTRUCTION_ZERO_SHOT,
#                 messages=[{"role": "user", "content": TEST_MESSAGE}])
#               -> next(b.text for b in response.content if b.type == "text")
#                  (claude-opus-5 thinks by default - filter by type,
#                  don't index response.content[0] directly)


# STEP 2 — one-shot: same as Step 1, but with STANDING_INSTRUCTION_ONE_SHOT.
# Again, three separate calls, print each output.


# STEP 3 — few-shot: same again, with STANDING_INSTRUCTION_FEW_SHOT. This
# time, one call is enough.


# STEP 4 — side-by-side comparison: print the message being tested, then
# all three zero-shot outputs, then all three one-shot outputs, then the
# few-shot output, so you can eyeball whether the answer got more
# consistent as examples were added.

# What this demonstrates:
# Zero-shot answers can wobble run to run on a borderline message. Adding
# worked examples - especially one that shows how to handle an ambiguous
# case with an honestly lower confidence score, rather than forcing false
# certainty - tends to pull repeated runs toward the same answer. Few-shot
# examples teach the *pattern* of a good answer, not just the rules for one.
