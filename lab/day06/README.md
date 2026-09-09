# Day 15 — GenAI frameworks with LangChain exercises

Six standalone exercises, one LangChain/LangGraph concept per file. Each
file uses the same running scenario for continuity: a hotel guest sends a
free-text message, and a LangGraph chain classifies what kind of request
it is, then responds to it appropriately. It's a stand-in for your own
Sprint 3 AI feature — wherever you see
`# [Placeholder — replace with your team's actual Sprint 3 AI feature]`,
that's the spot to swap in your own.

This builds directly on Day 12's prompt-engineering work (`lab/day03`):
the prompt wording used here is exactly the kind of already-tested prompt
a `PromptTemplate` packages for reuse. It does not re-teach how to write a
good prompt.

## Format

Each file is fully standalone (no shared code between files) and split
into two sections:

- **GIVEN** — the prompt text, sample data, and (from exercise 05 on) tool
  docstrings, already written out. You don't need to design these
  yourself.
- **YOUR TURN** — numbered `# STEP` comments describing what the code
  needs to do, with the exact LangChain/LangGraph class and method names
  to use. There's no code under these comments — you write it yourself,
  guided by the comment.

There are no answer files. Work through each `# STEP` comment in order and
run the file to see what you get.

## Setup

```bash
cd lab/day06
pip install -r requirements.txt
cp .env.example .env
# edit .env and fill in ANTHROPIC_API_KEY and/or OPENAI_API_KEY
```

You only need one key. Every exercise uses `init_chat_model("<provider>:<model>")`
from LangChain, which reads the right key automatically based on which
provider prefix you use — no separate code path per provider like Day 12's
exercises needed.

## Exercise order

| File | Concept |
|---|---|
| `01_prompt_templates.py` | `PromptTemplate` — parameterized, reusable prompts |
| `02_sequential_chain.py` | Chains — composing multi-step LLM calls with a fixed sequence |
| `03_branching_chain.py` | Conditional edges — routing to a different node based on state |
| `04_persistent_memory.py` | A checkpointer + `thread_id` — multi-turn memory across calls |
| `05_tool_integration.py` | `@tool`, `bind_tools`, `ToolNode` — one verified external call |
| `06_full_chain_capstone.py` | Putting it together: branch + memory + tool, one chain |

Work through them in order — each one builds on the mechanics from the one
before it, and `06` combines `03`, `04`, and `05` into a single working
skeleton.

## A note on API stability

LangChain went through a major redesign (v1) that moved its old `Chain`
classes (`LLMChain`, `ConversationChain`, ...) and memory classes
(`ConversationBufferMemory`, ...) into a separate `langchain-classic`
package for legacy code only. Every exercise here uses the current,
non-legacy building blocks (`PromptTemplate`, `StateGraph`, a checkpointer,
`@tool`) — if you find a tutorial online using `LLMChain` or
`ConversationBufferMemory`, it's written for the older API these exercises
deliberately don't use. This is a fast-moving library; if something here
stops matching LangChain's current docs, that's the library moving again,
not a typo in these files.
