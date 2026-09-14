"""
BONUS EXERCISE 10 — Evaluator-optimizer: a conditional edge that loops back on failure

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section for why it's included and cited from.

CONCEPT
-------
Confirmed directly against LangGraph's own current documentation ("Workflows
and agents"), EVALUATOR-OPTIMIZER is a named LangGraph pattern with a
concrete graph shape: a generator node produces a draft, an evaluator node
(a model call bound with structured output) grades it, and a conditional
edge on the evaluator's OWN output either exits the graph (the draft
passed) or loops back to the generator node with the evaluator's feedback
attached (the draft didn't pass yet) - LangGraph's own reference example
wires exactly this shape for a joke-writing generator and a funny/not-funny
evaluator. The loop-back edge here is mechanically the same idea exercise
02's decision loop already introduced (an edge pointing BACKWARD to a node
already visited) - the difference is WHAT triggers the loop. Exercise 02
loops because the model decided it needs another tool; this pattern loops
because a SEPARATE evaluator call judged the output not good enough yet.

This program has already built half of this pattern twice: Day 12's
guardrailed, structured-output pattern (a pydantic schema plus
with_structured_output, so a model's judgment comes back as a validated
field, not a string you have to parse by hand), and day07/06_reranking_eval.py's
RelevanceScore judge, which used exactly that pattern to SCORE a candidate
once. What's new here is looping inside an actual graph: instead of scoring
once and stopping, the evaluator's feedback is fed back into a
REGENERATION prompt via the loop-back edge, and the whole
generate-evaluate cycle repeats until the evaluator marks the response as
passing, or a state-held attempt count hits a bound - the same "don't loop
forever" discipline exercise 04 already built for the tool-calling agent,
now applied to a quality judgment instead.

This is also a useful contrast with exercise 06's retry step: exercise 06
retries an identical tool call after a FAILURE (an exception). This pattern
retries a DIFFERENT, improved generation after a QUALITY judgment (the
first attempt ran fine, it just wasn't good enough yet) - a different
reason to loop, with a different bound on how many times it's allowed to.

RUNNING SCENARIO
-----------------
Drafting a reply to a guest complaint, using an evaluator node to check
whether the draft is appropriately apologetic and offers a concrete next
step, looping back to the generator until it passes or a bound is hit.
# [Placeholder — replace with a generation task from your own Sprint 3
# agent task, e.g. drafting a maintenance-escalation message that must
# name a specific vendor and timeframe before it passes]

SETUP
-----
    pip install langchain langgraph pydantic python-dotenv
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

# STEP 0 — additional imports you'll need:
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
# YOUR CODE HERE


# STEP 1 — define DraftState, a TypedDict with five fields: complaint (str),
# draft (str), feedback (str), passes (bool), and attempt (int).
# YOUR CODE HERE


# STEP 2 — write generate_draft_node(state: DraftState) -> dict:
#   - build a feedback_section string: "" if state.get("feedback") is empty,
#     otherwise something like f"Address this specific feedback from the
#     last attempt: {state['feedback']}"
#   - format GENERATE_TEMPLATE_TEXT with state["complaint"] and that
#     feedback_section
#   - call model.invoke(...) to get a draft
#   - print the attempt number (state.get("attempt", 0) + 1) and the draft
#   - return {"draft": response.content, "attempt": state.get("attempt", 0) + 1}
def generate_draft_node(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 3 — write evaluate_draft_node(state: DraftState) -> dict:
#   - format EVALUATE_TEMPLATE_TEXT with state["complaint"] and state["draft"]
#   - call evaluator_model.invoke(...) to get an EvaluationResult
#   - print the evaluation (passes and feedback)
#   - return {"passes": result.passes, "feedback": result.feedback}
def evaluate_draft_node(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 4 — write route_evaluation(state: DraftState) -> str, the conditional
# edge function:
#   - if state["passes"] is True, return "Accepted"
#   - elif state["attempt"] >= MAX_ATTEMPTS, print a message saying the
#     bound was hit and return "Give up" (a bounded loop still needs to
#     stop and return something, exactly like exercise 04's step-bound
#     stop)
#   - otherwise, return "Retry"
def route_evaluation(state) -> str:
    # YOUR CODE HERE
    pass


# STEP 5 — build the graph:
#   - builder = StateGraph(DraftState)
#   - add generate_draft_node and evaluate_draft_node as nodes, naming them
#     "generate_draft" and "evaluate_draft"
#   - connect START to "generate_draft"
#   - connect "generate_draft" to "evaluate_draft" with a plain edge
#   - add a conditional edge from "evaluate_draft" using route_evaluation,
#     mapping "Accepted" -> END, "Give up" -> END, and "Retry" -> the SAME
#     "generate_draft" node - this is the loop-back edge that makes
#     regeneration happen with the evaluator's feedback attached
#   - compile the graph into `optimizer_graph`
# YOUR CODE HERE


# STEP 6 — invoke optimizer_graph with the initial state
# {"complaint": GUEST_COMPLAINT, "feedback": "", "attempt": 0} and print the
# final state's draft (the accepted draft, or the last one produced if the
# bound was hit).
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# The printed trace should show at least one attempt where passes is False
# with specific feedback (for example, "doesn't name a concrete next step"),
# followed by a regenerated draft (visible in generate_draft_node's own
# printed attempt number and text) that incorporates that feedback and
# passes on a later attempt - visible, attempt-by-attempt proof the
# loop-back edge is actually carrying the evaluator's feedback forward, not
# just re-running the same generation.
#
# Common Pitfalls:
# - An evaluator rubric so lax that EVERY draft passes on attempt 1 - that
#   never actually exercises the loop-back edge; GIVEN's rubric is
#   deliberately demanding for exactly this reason, matching this program's
#   own "your test case needs to surface a real difference" discipline
#   (day07/06_reranking_eval.py's own closing note made the same point
#   about evaluation query sets).
# - Mapping route_evaluation's "Retry" outcome to a NEW node instead of
#   back to "generate_draft" itself - that isn't a loop, it's just a longer
#   straight-line graph, and the evaluator's feedback never actually
#   reaches a second generation attempt.
# - No max_attempts bound checked inside route_evaluation at all - the
#   same indefinite-loop risk exercise 04's stopping-condition work exists
#   to prevent, here applied to a quality judgment instead of a
#   tool-calling decision.
#
# What this demonstrates:
# A second model call, dedicated ONLY to judging - never generating -
# catches quality problems a single generating call won't reliably
# self-correct on its own, the same principle behind day07's LLM-based
# reranker, now expressed as a real loop-back edge instead of a single
# score. Reach for this when "good enough on the first try" is not a safe
# assumption and a clear, checkable pass/fail rubric exists; reach for
# exercises 01-07's full agent loop when the task itself needs a variable
# NUMBER of different actions, not just a variable number of attempts at
# the same one.
"""
Sources:
- LangGraph: Workflows and agents (Evaluator-optimizer) — https://docs.langchain.com/oss/python/langgraph/workflows-agents
"""
