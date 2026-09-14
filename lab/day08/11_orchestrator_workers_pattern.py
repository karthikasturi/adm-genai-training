"""
BONUS EXERCISE 11 — Orchestrator-workers: dynamic fan-out with Send()

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section, including a scope note this exercise takes
particularly seriously.

CONCEPT
-------
Confirmed directly against LangGraph's own current documentation ("Workflows
and agents"), ORCHESTRATOR-WORKERS is a named LangGraph pattern for exactly
one situation exercise 09's parallelization can't handle: the NUMBER of
independent subtasks isn't known until an orchestrator call decomposes the
input at runtime. Because the fan-out is dynamic - not two fixed nodes
wired by hand the way exercise 09's graph is - LangGraph provides a
dedicated primitive for it: `Send(node_name, state)`, returned from a
function wired in with `add_conditional_edges`. Calling `Send("run_worker",
{"subtask": s})` once per subtask - however many the orchestrator decided
there are - dispatches that many copies of the SAME worker node to run in
the same superstep, each with its own slice of state. LangGraph's own
reference example uses exactly this shape for a report-writing
orchestrator that plans a variable number of sections, then fans out one
worker per section.

Collecting the workers' results back safely needs one more real piece:
LangGraph's own documentation names `operator.add` as the reducer used so
"multiple parallel nodes can safely append to the list without
conflicts" - each worker returns a one-item list, and the reducer
concatenates them into the running whole rather than one worker's return
value silently overwriting another's. This is the same "how do updates
combine instead of collide" question exercise 02's `add_messages` reducer
already answered for a running message list - here it's `operator.add` for
a running list of worker outputs instead.

SCOPE NOTE - read this before writing any code
-------------------------------------------------
Today's own course content is explicit that a "production-grade distributed
multi-agent system with more than one model coordinating" is OUT of scope
for Day 17 - today's agent (exercises 01-07) is one model choosing between
tools, not multiple agents. This exercise stays inside that boundary
deliberately: there is exactly ONE model in this file, and exactly ONE
compiled graph. "Orchestrator" and "worker" are two DIFFERENT NODES calling
that same model in two different ROLES (decompose, then answer one
subtask) - `Send()` dispatches multiple invocations of one worker NODE
inside one graph, not multiple independent agents or multiple models
coordinating. If you build this pattern for a real Sprint 3 task, keep
that same distinction in mind.

RUNNING SCENARIO
-----------------
A multi-part guest question the orchestrator node breaks into subtasks
whose number ISN'T fixed in advance (unlike exercise 09's exactly-two-tasks
case) - each subtask fanned out to its own worker node via Send(), then
synthesized into one reply.
# [Placeholder — replace with a genuinely decomposable task from your own
# Sprint 3 agent task, e.g. Meridian Kitchens Collective's reorder-drafting
# task broken into "check current stock," "identify the right supplier,"
# and "draft the request," a number of subtasks that could plausibly vary]

SETUP
-----
    pip install langchain langgraph pydantic python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the orchestrator's decomposition schema and prompts. Nothing to
# change here.
# =============================================================================

import operator
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
    "exercise is about the DECOMPOSE-DISPATCH-SYNTHESIZE shape, not about "
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

# STEP 0 — additional imports you'll need:
#   from typing import Annotated
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
#   from langgraph.types import Send
# YOUR CODE HERE


# STEP 1 — define two TypedDicts:
#   - OrchestratorState: question (str), subtasks (list[str]),
#     subanswers (Annotated[list, operator.add]), final_answer (str)
#   - WorkerState: subtask (str), subanswers (Annotated[list, operator.add])
# (Both states share the "subanswers" field name and reducer on purpose -
# that's what lets a worker's single-item return list merge into the same
# running list the orchestrator's own state exposes after fan-in.)
# YOUR CODE HERE


# STEP 2 — write decompose(state: OrchestratorState) -> dict:
#   - format DECOMPOSE_TEMPLATE_TEXT with state["question"]
#   - call orchestrator_model.invoke(...) to get a Subtasks object
#   - print the list of subtasks it returned
#   - return {"subtasks": result.subtasks}
def decompose(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 3 — write assign_workers(state: OrchestratorState) -> list[Send]:
# the fan-out function `add_conditional_edges` will call. For each subtask
# in state["subtasks"], build one
# Send("run_worker", {"subtask": subtask}) and return the full list -
# exactly one Send per subtask, however many there turned out to be.
def assign_workers(state) -> list:
    # YOUR CODE HERE
    pass


# STEP 4 — write run_worker(state: WorkerState) -> dict: format
# WORKER_TEMPLATE_TEXT with state["subtask"], call model.invoke(...) (the
# plain model, in its WORKER role this time - not orchestrator_model), and
# return {"subanswers": [response.content]} - a ONE-ITEM list, so the
# operator.add reducer can concatenate each worker's single answer into
# the shared running list instead of one worker overwriting another.
def run_worker(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 5 — write synthesize(state: OrchestratorState) -> dict:
#   - build one "subanswers" string joining each subtask with its matching
#     subanswer, one per line (e.g. f"- {subtask}: {subanswer}" - zip
#     state["subtasks"] with state["subanswers"])
#   - format SYNTHESIZE_TEMPLATE_TEXT with state["question"] and that
#     joined string
#   - call model.invoke(...) and return {"final_answer": response.content}
def synthesize(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 6 — build the graph:
#   - builder = StateGraph(OrchestratorState)
#   - add decompose, run_worker, and synthesize as nodes, naming them
#     "decompose", "run_worker", and "synthesize"
#   - connect START to "decompose"
#   - add a conditional edge from "decompose" using assign_workers, listing
#     "run_worker" as its only possible destination (LangGraph's own
#     Send-based add_conditional_edges call takes the destination list as
#     its third argument: add_conditional_edges("decompose", assign_workers, ["run_worker"]))
#   - connect "run_worker" to "synthesize" with a plain edge
#   - connect "synthesize" to END
#   - compile the graph into `orchestrator_graph`
# YOUR CODE HERE


# STEP 7 — invoke orchestrator_graph with
# {"question": MULTI_PART_QUESTION, "subanswers": []} and print the final
# state's final_answer. Then, as a comment, answer this: exercise 09's two
# tool calls were fanned out from START with two hand-wired edges, known in
# advance; this exercise's fan-out is dynamic, decided by assign_workers at
# RUN TIME. What would have to be true about MULTI_PART_QUESTION for
# exercise 09's fixed two-edge shape to have worked instead of needing
# Send() at all?
# YOUR CODE HERE (and your answer, as a comment)


# EXPECTED RESULT
# ----------------
# decompose should produce a NUMBER of subtasks that genuinely reflects the
# input (three, for MULTI_PART_QUESTION as given - but rerun with a
# two-part or four-part question and confirm the count actually changes,
# proving this is real decomposition, not a fixed-count template, and that
# assign_workers really does dispatch a different NUMBER of Send() calls
# each time). The final synthesized reply should read as ONE coherent
# answer, not three pasted-together fragments.
#
# Common Pitfalls:
# - Returning a bare list of dicts from assign_workers instead of a list of
#   real Send(...) objects - add_conditional_edges expects Send instances
#   here specifically because that's what tells the runtime which NODE
#   each dispatched piece of state should go to.
# - Forgetting the Annotated[list, operator.add] reducer on subanswers in
#   BOTH state definitions - without it, each worker's return value
#   overwrites the shared list instead of appending to it, and synthesize
#   sees only whichever worker happened to finish last.
# - Treating `orchestrator_model` and the worker calls in run_worker as
#   different MODELS or different AGENTS - re-read the SCOPE NOTE above.
#   There is one model here, invoked from two different nodes in two
#   different roles, not a multi-agent system.
# - Testing only with MULTI_PART_QUESTION and never confirming the subtask
#   COUNT actually varies with a different input - a hard-coded three-part
#   decomposition dressed up as dynamic is not what this pattern is for.
"""
Sources:
- LangGraph: Workflows and agents (Orchestrator-worker) — https://docs.langchain.com/oss/python/langgraph/workflows-agents
"""
