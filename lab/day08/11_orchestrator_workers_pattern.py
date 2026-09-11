"""
BONUS EXERCISE 11 — Orchestrator-workers: one model decomposing and delegating

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section, including a scope note this exercise takes
particularly seriously.

CONCEPT
-------
Anthropic's "Building Effective Agents" names ORCHESTRATOR-WORKERS as a
workflow pattern where a central LLM call dynamically breaks a task into
subtasks, delegates each to a WORKER LLM call, then synthesizes the
results - well suited to tasks where the subtasks genuinely can't be
predicted in advance (unlike exercise 09's parallelization, where the two
independent pieces of work were already known up front).

SCOPE NOTE - read this before writing any code
-------------------------------------------------
Today's own course content is explicit that a "production-grade distributed
multi-agent system with more than one model coordinating" is OUT of scope
for Day 17 - today's agent (exercises 01-07) is one model choosing between
tools, not multiple agents. This exercise stays inside that boundary
deliberately: there is exactly ONE model in this file. "Orchestrator" and
"worker" are two DIFFERENT PROMPTS sent to that same model in two different
ROLES (decompose, then answer one subtask), not two different agents or two
different models coordinating. If you build this pattern for a real Sprint
3 task, keep that same distinction in mind - a worker call is still just an
LLM call your own code invokes and collects the result from, not an
independent, autonomous agent making its own tool-calling decisions the way
exercises 01-07's loop does.

RUNNING SCENARIO
-----------------
A multi-part guest question the orchestrator call breaks into subtasks
whose number ISN'T fixed in advance (unlike exercise 09's exactly-two-tasks
case) - each subtask answered by a worker call, then synthesized into one
reply.
# [Placeholder — replace with a genuinely decomposable task from your own
# Sprint 3 agent task, e.g. Meridian Kitchens Collective's reorder-drafting
# task broken into "check current stock," "identify the right supplier,"
# and "draft the request," a number of subtasks that could plausibly vary]

SETUP
-----
    pip install langchain pydantic python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the orchestrator's decomposition schema and prompts. Nothing to
# change here.
# =============================================================================

from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"

model = init_chat_model(CHAT_MODEL)

MULTI_PART_QUESTION = (
    "Before I book, I need to know: is the spa open the day I arrive, "
    "can I bring my dog to dinner, and what's your cancellation policy "
    "if my flight gets delayed?"
)

class Subtasks(BaseModel):
    subtasks: list[str] = Field(description="A list of independent, self-contained sub-questions this task decomposes into - one per distinct piece of information genuinely being asked for")

orchestrator_model = model.with_structured_output(Subtasks)

DECOMPOSE_TEMPLATE_TEXT = (
    "Break this guest question down into a list of independent, "
    "self-contained sub-questions - one per distinct piece of information "
    "being asked for. Don't merge unrelated questions into one item, and "
    "don't split one single question into pieces that depend on each other.\n\n"
    "Guest question: {question}"
)

WORKER_TEMPLATE_TEXT = (
    "Answer this single guest sub-question as a short, standalone statement: {subtask}\n\n"
    "(You may not have real data for this - answer plausibly and clearly "
    "mark any part you're inferring rather than looking up, since this "
    "exercise is about the DECOMPOSE-DELEGATE-SYNTHESIZE shape, not about "
    "wiring in real tools - exercises 01-07 already cover real tool calls.)"
)

SYNTHESIZE_TEMPLATE_TEXT = (
    "Combine these separately-answered sub-questions into ONE coherent, "
    "well-organized reply to the guest's original question.\n\n"
    "Original question: {question}\n\nSub-answers:\n{subanswers}"
)

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — write decompose(question: str) -> list[str]:
#   - format DECOMPOSE_TEMPLATE_TEXT with the question
#   - call orchestrator_model.invoke(...) to get a Subtasks object
#   - print the list of subtasks it returned
#   - return result.subtasks
def decompose(question: str) -> list[str]:
    # YOUR CODE HERE
    pass


# STEP 2 — write run_worker(subtask: str) -> str: format
# WORKER_TEMPLATE_TEXT with the subtask, call model.invoke(...) (the plain
# model, in its WORKER role this time - not orchestrator_model), and return
# the response's .content.
def run_worker(subtask: str) -> str:
    # YOUR CODE HERE
    pass


# STEP 3 — write synthesize(question: str, subtasks: list[str], subanswers:
# list[str]) -> str:
#   - build one "subanswers" string joining each subtask with its matching
#     subanswer, one per line (e.g. f"- {subtask}: {subanswer}")
#   - format SYNTHESIZE_TEMPLATE_TEXT with the original question and that
#     joined string
#   - call model.invoke(...) and return the response's .content
def synthesize(question: str, subtasks: list[str], subanswers: list[str]) -> str:
    # YOUR CODE HERE
    pass


# STEP 4 — write orchestrate(question: str) -> str, tying the three
# functions together:
#   - subtasks = decompose(question)
#   - subanswers = [run_worker(t) for t in subtasks] (a plain loop is fine
#     here - Step 5 asks you to reconsider that choice)
#   - return synthesize(question, subtasks, subanswers)
def orchestrate(question: str) -> str:
    # YOUR CODE HERE
    pass


# STEP 5 — call orchestrate(MULTI_PART_QUESTION) and print the final
# synthesized reply. Then, as a comment, answer this: each worker call in
# Step 4 is independent of the others (none needs another's result) - could
# Step 4's list comprehension be replaced with exercise 09's
# ThreadPoolExecutor pattern to run all worker calls concurrently instead of
# in a loop? What would have to be true about the subtasks for that to be
# safe?
# YOUR CODE HERE (and your answer, as a comment)


# EXPECTED RESULT
# ----------------
# decompose should produce a NUMBER of subtasks that genuinely reflects the
# input (three, for MULTI_PART_QUESTION as given - but rerun with a
# two-part or four-part question and confirm the count actually changes,
# proving this is real decomposition, not a fixed-count template). The
# final synthesized reply should read as ONE coherent answer, not three
# pasted-together fragments.
#
# Common Pitfalls:
# - Treating `orchestrator_model` and the worker calls in run_worker as
#   different MODELS or different AGENTS - re-read the SCOPE NOTE above.
#   There is one model here, called in two different roles; conflating this
#   with a genuine multi-agent system misrepresents both this pattern and
#   today's own explicit out-of-scope boundary.
# - Testing only with MULTI_PART_QUESTION and never confirming the subtask
#   COUNT actually varies with a different input - a hard-coded three-part
#   decomposition dressed up as dynamic is not what this pattern is for.
# - Reaching for this pattern when exercise 09's parallelization already
#   fits better - if the subtasks are already known and fixed in advance
#   (like exercise 01's two tools), you don't need a decomposition call at
#   all; orchestrator-workers earns its extra LLM call specifically when the
#   subtask breakdown itself can't be predicted ahead of time.
"""
Sources:
- Anthropic: Building Effective Agents — https://www.anthropic.com/engineering/building-effective-agents
"""
