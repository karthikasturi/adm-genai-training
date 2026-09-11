# Day 17 — Agentic AI workflows & orchestration exercises

Twelve standalone exercises: seven core exercises (one agentic-loop concept
per file), four bonus exercises on other agentic workflow patterns, and one
core-adjacent exercise comparing the hand-built loop against LangChain's
prebuilt `create_agent` (see below for both). Each file uses the same
running scenario for continuity: the same
hospitality guest-facing assistant from Days 15-16, now given BOTH of its
previously-built tools at once and let loose in a real decision loop. It's a
stand-in for your own Sprint 3 agent — wherever you see
`# [Placeholder — replace with your team's actual Sprint 3 agent task]`,
that's the spot to swap in your own.

This builds directly on Day 15's tool-integration work (`lab/day06`) and
Day 16's retrieval pipeline (`lab/day07`): both tools —
`get_reservation` (Module 15B) and `answer_guest_question` (Module 16B) —
are reused **exactly as already built and verified**, not reinvented. The
whole point of today's exercises is the difference between "we called this
tool once, and it worked" and "the model now decides for itself, repeatedly,
whether to call it."

## Format — different from `lab/day07`

Each file is fully standalone (no shared code between files) and split into
two sections:

- **GIVEN** — the sample data, tools, and scenario, already written out and
  working. You don't need to design or debug these yourself.
- **YOUR TURN** — numbered `# STEP` comments describing exactly what the
  code needs to do, naming the exact class/method/attribute to use.

**Unlike `lab/day07`, the YOUR TURN code is *not* filled in here.** Each
step is a comment only; function signatures are stubbed with `pass`, and
module-level steps are marked `# YOUR CODE HERE`. Write the real
implementation yourself under each step, using the exact names the comment
gives you. There are no separate answer files — the steps live in the file,
the code is yours to write.

## Setup

```bash
cd lab/day08
pip install -r requirements.txt
cp .env.example .env
# edit .env and fill in OPENAI_API_KEY (required) and, optionally,
# ANTHROPIC_API_KEY
```

## Core exercise order (the graded Day 17 outline)

Mirrors `course-outline/Day17_Agentic_AI_Workflows_Orchestration_Content.md`
— Module 17A (Agent Decision Loops) and Module 17B (Stopping Conditions,
Multi-Tool Agents & Recovery) — one exercise per topic/hands-on phase.

| File | Concept |
|---|---|
| `01_multi_tool_binding.py` | Why a fixed chain can't handle a variable step count; binding two tools with `bind_tools([...])`, inspecting `tool_calls` |
| `02_decision_loop.py` | `AgentState`, `call_model`, `ToolNode`, `tools_condition`, and the one new shape: an edge back to `call_model` that closes the loop |
| `03_loop_verification.py` | Proving it's a real loop: a one-tool message vs. a two-tool message, counting `call_model` visits |
| `04_stopping_conditions.py` | Task completion vs. a bounded-step failsafe: a state-held `step_count`, plus `recursion_limit` as the safety net underneath |
| `05_multi_tool_choice.py` | Verifying correct tool choice on clearly-scoped test messages; fixing a wrong choice via the tool's docstring |
| `06_retry_recovery.py` | A hand-written retry wrapper: catch a real tool-execution failure, reissue once, give up cleanly if it fails again |
| `07_diagnose_failure.py` | Capstone: everything above combined, run against one adversarial test message, diagnosing a loop or a wrong-tool-call failure from the printed trace |

Work through them in order — `02` builds the loop `03` verifies, `04` adds
the stopping condition on top of `02`/`03`'s shape, `05` and `06` each add
one more piece to that same shape, and `07` combines every piece into one
finished agent and tests it adversarially.

## Bonus: agentic workflow patterns

*Exercises `08`–`11` are enrichment, beyond the graded Day 17 outline.* The
outline itself is deliberately tight (10 minutes of slack against the
realistic daily ceiling) and explicitly scopes today's agent to one model
choosing between tools — not a survey of every agentic architecture. These
four exercises fill a genuine gap the course otherwise never covers: they
teach Anthropic's own named **workflow** patterns (LLMs orchestrated through
*predefined* code paths), as distinct from the full **agent** (the LLM
*dynamically* directs its own process) exercises `01`–`07` build. Prompt
chaining, the fifth pattern in that same reference, is not repeated here —
it's already `lab/day06/02_sequential_chain.py` (Day 15).

| File | Pattern |
|---|---|
| `08_routing_pattern.py` | Routing: a hard-coded keyword router vs. a model-based router, on a message the keyword version can't classify |
| `09_parallelization_pattern.py` | Parallelization (sectioning): two independent tool calls run concurrently instead of sequentially, with measured timing |
| `10_evaluator_optimizer_pattern.py` | Evaluator-optimizer: generate → structured-output critique → regenerate, looping until a rubric passes |
| `11_orchestrator_workers_pattern.py` | Orchestrator-workers: one model decomposes a task into a *variable* number of subtasks, delegates each as a worker call, synthesizes the results |

**A scope note worth reading before `11`:** today's own course content is
explicit that a distributed multi-agent system with more than one model
coordinating is out of scope for Day 17. `11_orchestrator_workers_pattern.py`
stays inside that boundary deliberately — there is exactly **one** model in
that file, called in two different roles (orchestrator, then worker), not
multiple agents. The file's own scope note says this again, in place, before
any code.

**Sources:**
- [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

## Core-adjacent: `create_agent` comparison

| File | Concept |
|---|---|
| `12_create_agent_comparison.py` | The exact agent from exercises 02/04/06, rebuilt with LangChain's prebuilt `create_agent` and its `ModelCallLimitMiddleware`/`ToolRetryMiddleware`, compared side by side with the hand-built version |

Unlike `08`–`11`, this one isn't an outside addition — the Day 17 course
content's own Assumption 1 explicitly commits to introducing `create_agent`
fully "once the loop, the stopping condition, and the tool set it wraps have
all been built and seen working by hand," i.e. exactly after exercise 07.
It isn't one of the outline's six graded hands-on lines either, which is why
it's numbered after the bonus patterns rather than folded into 01–07.

## A note on the two reused tools

`get_reservation` and `answer_guest_question` appear, unchanged, in the
GIVEN section of nearly every file (exercise `05` is the one exception — its
whole point is testing and, if needed, revising `get_reservation`'s
docstring). This repetition matches `lab/day07`'s own standalone-file
convention (each file rebuilds what it needs rather than importing from a
sibling file) and is also today's own explicit design choice, not an
oversight: reusing two tools you already built and personally verified two
days ago is what makes today's actual new lesson — "the model decides for
itself, repeatedly, whether and when to call this" — visible against a tool
whose own correctness isn't in question.

## A note on `recursion_limit` vs. the state-based step bound

`04_stopping_conditions.py` builds a designed, graceful stop (a `step_count`
field, checked in the same routing function that already checks
`tools_condition`) rather than relying on LangGraph's own graph-wide
`recursion_limit` alone. Both matter and both are used together: the
state-based bound is what you're building and testing; `recursion_limit`,
set at a comfortably higher value in the run config, stays underneath it as
a safety net against a bug in that state-based logic itself — belt and
suspenders, not either-or, exactly as
`course-outline/Day17_Agentic_AI_Workflows_Orchestration_Content.md`'s own
Assumption 4 lays out.

## A note on what's deliberately built by hand vs. named as the production version

Exercises 01–07 build every mechanism by hand — the loop itself, the
step-bound routing function, the retry wrapper — rather than starting from
LangChain's prebuilt `create_agent` or its middleware stack
(`ToolRetryMiddleware`, `ModelCallLimitMiddleware`, `HumanInTheLoopMiddleware`,
and others). That's a deliberate choice carried over from Days 15-16's own
primitives-first approach, not an oversight: `create_agent`'s own loop is a
black box once called, and the point of exercises 01–07 is to make the
actual routing decision — tool call or stop? — code you write and can read
back. Exercise 12 is where `create_agent` itself finally gets built, once
that underlying shape is already understood — the same sequencing Days 15–16
already used for LCEL relative to `StateGraph`. See
`course-outline/Day17_Agentic_AI_Workflows_Orchestration_Content.md` for the
full grounding and current documentation links.
