# Day 12 — prompt engineering exercises

Six standalone exercises, one prompt-engineering concept per file. Each
file uses the same running scenario for continuity: classifying an inbound
customer support message into `Billing`, `Technical`, or `General`, with a
confidence score (0–1) and a one-sentence reason. It's a stand-in for a
real feature — wherever you see
`# [Placeholder — replace with your own task]`, that's the spot to swap in
your own.

## Format

Each file is fully standalone (no shared code between files) and split
into two sections:

- **GIVEN** — the prompt text, test data, and schema for that exercise,
  already written out. You don't need to design these yourself.
- **YOUR TURN** — numbered `# STEP` comments describing what the code
  needs to do, with the exact method/parameter names to use for both
  OpenAI and Anthropic. There's no code under these comments — you write
  it yourself, guided by the comment.

There are no answer files. Work through each `# STEP` comment in order and
run the file to see what you get.

## Setup

Requires Python 3.10+ (needed by the current `anthropic` SDK major version).

```bash
cd lab/day03
pip install -r requirements.txt
cp .env.example .env
# edit .env and fill in OPENAI_API_KEY and/or ANTHROPIC_API_KEY
```

You only need one key, but every exercise's comments cover both providers
— pick whichever you have.

## Exercise order

| File | Concept |
|---|---|
| `01_prompt_structure.py` | Standing instructions vs. the specific request |
| `02_few_shot_examples.py` | Zero-shot vs. few-shot |
| `03_iterative_refinement.py` | run → observe → revise → re-run |
| `04_evaluate_test_set.py` | Scoring prompt versions against a fixed test set |
| `05_guardrails.py` | Defending a prompt against adversarial input |
| `06_structured_output_schema.py` | From "asks for JSON" to "guarantees JSON" |

Work through them in order — each one reuses the prompt built in the one
before it.
