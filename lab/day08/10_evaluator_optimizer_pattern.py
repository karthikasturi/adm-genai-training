"""
BONUS EXERCISE 10 — Evaluator-optimizer: generate, critique, regenerate until it passes

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section for why it's included and cited from.

CONCEPT
-------
Anthropic's "Building Effective Agents" names EVALUATOR-OPTIMIZER as a
workflow pattern where one LLM call GENERATES a response while a SEPARATE
LLM call EVALUATES it and provides feedback, looping until the evaluator is
satisfied (or a bounded attempt count is reached - the same "don't loop
forever" discipline exercise 04 already built for the tool-calling agent).

This program has already built half of this pattern twice: Day 12's
guardrailed, structured-output pattern (a pydantic schema plus
with_structured_output, so a model's judgment comes back as a validated
field, not a string you have to parse by hand), and day07/06_reranking_eval.py's
RelevanceScore judge, which used exactly that pattern to SCORE a candidate
once. What's new here is looping: instead of scoring once and stopping, the
evaluator's feedback is fed back into a REGENERATION prompt, and the whole
generate-evaluate cycle repeats until the evaluator marks the response as
passing, or a max-attempts bound is hit.

This is also a useful contrast with exercise 06's retry step: exercise 06
retries an identical tool call after a FAILURE (an exception). This pattern
retries a DIFFERENT, improved generation after a QUALITY judgment (the
first attempt ran fine, it just wasn't good enough yet) - a different
reason to loop, with a different bound on how many times it's allowed to.

RUNNING SCENARIO
-----------------
Drafting a reply to a guest complaint, using an evaluator call to check
whether the draft is appropriately apologetic and offers a concrete next
step, regenerating until it passes or a bound is hit.
# [Placeholder — replace with a generation task from your own Sprint 3
# agent task, e.g. drafting a maintenance-escalation message that must
# name a specific vendor and timeframe before it passes]

SETUP
-----
    pip install langchain pydantic python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the generation prompt, the evaluator's schema, and a deliberately
# demanding rubric (so a first draft plausibly fails at least once,
# something worth proving rather than assuming). Nothing to change here.
# =============================================================================

from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
MAX_ATTEMPTS = 3

model = init_chat_model(CHAT_MODEL)

GUEST_COMPLAINT = "The room wasn't cleaned before I checked in and nobody has followed up."

GENERATE_TEMPLATE_TEXT = (
    "Draft a short reply to this guest complaint: {complaint}\n\n"
    "{feedback_section}"
)

class EvaluationResult(BaseModel):
    passes: bool = Field(description="True only if the reply is genuinely apologetic AND names a concrete next step (a specific action or timeframe), not a vague promise")
    feedback: str = Field(description="One or two sentences of specific, actionable feedback for the next draft - empty if passes is True")

evaluator_model = model.with_structured_output(EvaluationResult)

EVALUATE_TEMPLATE_TEXT = (
    "Evaluate this draft reply to a guest complaint.\n\n"
    "Complaint: {complaint}\n\nDraft reply: {draft}\n\n"
    "It passes ONLY if it is genuinely apologetic AND names a concrete next "
    "step (a specific action or timeframe) - not merely a vague apology."
)

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — write generate_draft(complaint: str, feedback: str = "") -> str:
#   - build a feedback_section string: "" if feedback is empty, otherwise
#     something like f"Address this specific feedback from the last
#     attempt: {feedback}"
#   - format GENERATE_TEMPLATE_TEXT with complaint and that feedback_section
#   - call model.invoke(...) and return the response's .content
def generate_draft(complaint: str, feedback: str = "") -> str:
    # YOUR CODE HERE
    pass


# STEP 2 — write evaluate_draft(complaint: str, draft: str) -> EvaluationResult:
#   - format EVALUATE_TEMPLATE_TEXT with complaint and draft
#   - call evaluator_model.invoke(...) and return the EvaluationResult
def evaluate_draft(complaint: str, draft: str) -> EvaluationResult:
    # YOUR CODE HERE
    pass


# STEP 3 — write generate_with_evaluation(complaint: str, max_attempts: int =
# MAX_ATTEMPTS) -> str, the actual evaluator-optimizer loop:
#   - start with feedback = ""
#   - for each attempt up to max_attempts:
#       - call generate_draft(complaint, feedback) to get a draft
#       - call evaluate_draft(complaint, draft) to get an EvaluationResult
#       - print the attempt number, the draft, and the evaluation
#       - if result.passes is True, return the draft immediately
#       - otherwise, set feedback = result.feedback for the next attempt
#   - if no attempt passes within max_attempts, print a message saying so
#     and return the LAST draft produced anyway (a bounded loop still needs
#     to return something, exactly like exercise 04's step-bound stop)
def generate_with_evaluation(complaint: str, max_attempts: int = MAX_ATTEMPTS) -> str:
    # YOUR CODE HERE
    pass


# STEP 4 — call generate_with_evaluation(GUEST_COMPLAINT) and print the
# final accepted (or last) draft.
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# The printed trace should show at least one attempt where passes is False
# with specific feedback (for example, "doesn't name a concrete next step"),
# followed by a regenerated draft that incorporates that feedback and passes
# on a later attempt - visible, attempt-by-attempt proof the loop is
# actually using the evaluator's feedback, not just retrying blindly.
#
# Common Pitfalls:
# - An evaluator rubric so lax that EVERY draft passes on attempt 1 - that
#   never actually exercises the loop; GIVEN's rubric is deliberately
#   demanding for exactly this reason, matching this program's own
#   "your test case needs to surface a real difference" discipline
#   (day07/06_reranking_eval.py's own closing note made the same point
#   about evaluation query sets).
# - Ignoring result.feedback on the next attempt (calling generate_draft
#   with feedback="" every time) - that turns this into "just retry and
#   hope," not evaluator-guided OPTIMIZATION.
# - No max_attempts bound at all - the same indefinite-loop risk
#   exercise 04's stopping-condition work exists to prevent, here applied
#   to a quality judgment instead of a tool-calling decision.
#
# What this demonstrates:
# A second LLM call, dedicated ONLY to judging - never generating - catches
# quality problems a single generating call won't reliably self-correct on
# its own, the same principle behind day07's LLM-based reranker, now looped
# instead of run once. Reach for this when "good enough on the first try" is
# not a safe assumption and a clear, checkable pass/fail rubric exists;
# reach for exercises 01-07's full agent loop when the task itself needs a
# variable NUMBER of different actions, not just a variable number of
# attempts at the same one.
"""
Sources:
- Anthropic: Building Effective Agents — https://www.anthropic.com/engineering/building-effective-agents
"""
