# Day 13 Lab Guide: LLMs, Responsible AI & AI-Assisted Coding

Source content: `presentation/Day13_LLMs_Responsible_AI_AI_Coding.pptx` speaker notes (no course-content-architect content doc on record for Day 13 — this guide reads the deck and its notes directly, plus the working code from `lab/day03` — Day 12's prompt-engineering lab — which Module 13A's Exercise 1 extends). Each exercise below is self-contained — work through any one of them with nothing else open but this document.

## Module 1: LLM Capabilities, Limits & Responsible Use

### Exercise 1: Compare two models' reasoning, cost & hallucination trade-offs
**Objective:**
By the end of this exercise, you will have sent the same test message through Day 12's schema-constrained prompt against two different model tiers — one per vendor, or two tiers from the same vendor — and recorded each one's classification, confidence, schema compliance, and token usage, so the difference between tiers is something you've seen happen to your own prompt, not just a row on a comparison table.

**Prerequisites for this exercise:**
- `lab/day03/06_structured_output_schema.py` must already work (Day 12's completed exercise) — this exercise reuses its `GUARDED_INSTRUCTION` and `SCHEMA` constants unchanged.
- `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY` set, same as Day 12.
- The exact model ID strings for the two tiers you want to compare, from this morning's model-family comparison or your account's current model list: **[Placeholder — replace with your account's exact model ID strings for the two tiers you're comparing]**.

**Steps:**
1. In your terminal, run `mkdir -p lab/day04 && cd lab/day04` and create a new file named `01_compare_models.py`.
2. At the top of the file, copy the `GUARDED_INSTRUCTION` and `SCHEMA` constants from `lab/day03/06_structured_output_schema.py` exactly as they are, with no changes.
3. Add the same imports and client setup as `lab/day03/06_structured_output_schema.py` Step 0: `from openai import OpenAI`, `import anthropic`, `import json`, `client_openai = OpenAI()`, `client_anthropic = anthropic.Anthropic()`.
4. Add one new constant: `TEST_MESSAGE = "My payment went through but the service still says it's disabled."`
5. Write the two model ID strings you picked from this morning's comparison into two constants, for example `MODEL_A = "..."` and `MODEL_B = "..."` — replace the `...` with the real IDs from your Prerequisites placeholder above.
6. For an OpenAI model ID, call `client_openai.responses.create(model=MODEL_ID, input=[{"role": "developer", "content": GUARDED_INSTRUCTION}, {"role": "user", "content": TEST_MESSAGE}], text={"format": {"type": "json_schema", "name": "classification", "schema": SCHEMA, "strict": True}})`, matching Exercise 6, Step 2's shape exactly.
7. For an Anthropic model ID, call `client_anthropic.messages.create(model=MODEL_ID, max_tokens=300, system=GUARDED_INSTRUCTION, messages=[{"role": "user", "content": TEST_MESSAGE}], output_config={"format": {"type": "json_schema", "schema": SCHEMA}})`, matching the same step's Anthropic shape.
8. For each of your two model IDs, call the matching function from step 6 or 7, then run `json.loads()` on the result inside a `try`/`except` and print whether it succeeded.
9. For each call, also print its token usage (`response.usage` on both vendors' response objects) as your stand-in for cost.
10. Run the script with `python 01_compare_models.py` and confirm it prints one full result block — category, confidence, schema-compliance, token usage — for each of the two model IDs, with no unhandled exception.
11. Compare the two printed blocks and write one sentence naming a concrete difference between them (for example, a confidence gap, a schema-compliance failure on one side, or a token-usage difference for the same message).

**Expected Result:**
The script prints two complete result blocks, one per model tier, each showing category, confidence, whether `json.loads()` succeeded, and token usage, with no unhandled exception — and you have one written sentence naming a real, observed difference between the two tiers' answers to the same message.

**Troubleshooting:**
- **Both calls return `General` with low confidence** → You're likely still using yesterday's `ADVERSARIAL_MESSAGE` instead of the new `TEST_MESSAGE` — a good-faith message should classify as `Billing` or `Technical`, not fall through to `General`.
- **`json.JSONDecodeError` still raised even with a schema attached** → Check that you used the right argument name for each vendor — `text={"format": {...}}` for OpenAI's Responses API, `output_config={"format": {...}}` for Anthropic's Messages API. These are not interchangeable.
- No other common pitfalls noted for this exercise.

### Exercise 2: Identify a hallucination risk specific to the capstone's use case
**Objective:**
By the end of this exercise, you will have named one concrete way your own capstone's AI feature could state something false with confidence, correctly diagnosed it as either a missing-fact problem or a consistency problem, and picked the matching category of fix — before touching any code.

**Prerequisites for this exercise:**
None beyond the course prerequisites. Have your capstone's actual AI-assisted feature (for example, the ticket classifier built in Day 12) in mind before starting.

**Steps:**
1. As a team, open the shared document tracking your capstone's architecture.
2. Reread your capstone's actual AI feature and write down one concrete, specific way the model could state something false with full confidence about a real case — not a hypothetical category of error, an actual example you can picture happening.
3. Ask: if the model already had the exact right document, record, or fact available to it right now, would it definitely get this case right? If yes, this is a **consistency problem** — the model has the fact but states it unreliably.
4. If the answer to step 3 is no — the model has no way to know the true fact at all because it was never given the document, database record, or context containing it — mark this instead as a **missing-fact problem**.
5. Write one sentence stating which of the two you picked, using the specific example from step 2 as evidence.
6. Below that sentence, name the matching fix: retrieval (give the model the missing document or record) for a missing-fact problem, or prompting/fine-tuning (make it use what it already has more reliably) for a consistency problem — and write one more sentence saying why the other category of fix wouldn't actually solve this case.
7. Save the document.

**Expected Result:**
The shared document names one hallucination risk specific to your own capstone feature, correctly diagnosed as a missing-fact or consistency problem, with the matching fix category and a one-sentence justification for both the diagnosis and why the other fix category wouldn't work.

**Troubleshooting:**
- **Not sure which category it is** → Ask "if I handed the model the exact right document or record right now, would it definitely get this right?" A "yes" is a consistency problem (retrieval won't help); a "no" is a missing-fact problem (retrieval will).
- **Picked retrieval as the fix for a consistency problem** → This is a real, documented mistake: adding retrieval to a model that already has the fact but states it unreliably can decrease performance rather than improve it. Go back to steps 3–4 and re-diagnose before picking a fix.
- No other common pitfalls noted for this exercise.

### Exercise 3: Run the safety and bias checklist against an earlier model output
**Objective:**
By the end of this exercise, you will have walked one real model output from Exercise 1 through all five safety-and-bias checklist questions, answering each with a yes/no and one sentence of real evidence — not a bare checkmark.

**Prerequisites for this exercise:**
At least one saved model output from Module 1, Exercise 1 (the classification result for `TEST_MESSAGE`).

**Steps:**
1. Open the output you recorded in Exercise 1 for one of the two model tiers you tested.
2. Answer "Has a human actually read this, not just skimmed the confidence score?" with yes or no, plus one sentence of evidence — for example, whether you actually read the `reason` field or only glanced at `confidence`.
3. Answer "Was it tested against at least one adversarial or edge-case input?" — if you haven't already, run `ADVERSARIAL_MESSAGE` from `lab/day03/05_guardrails.py` through the same model and use that as your evidence.
4. Answer "Does it show any sign of the bias the last topic named (political evenhandedness, minor protections, or care for a distressed user)?" by rereading the actual `reason` text for any of those three signs.
5. Answer "Does the prompt already constrain tone/topic, or is safety doing the prompt's job?" by checking whether `GUARDED_INSTRUCTION`'s own Guardrail clause actually covers this case, or whether you're relying on a human catching it instead.
6. Answer "Is there a real, monitored way for a user to flag a bad output?" based on your capstone's actual current design, not a hypothetical future feature.
7. Save all five answers, each with its one-sentence evidence, in the same shared document as Exercise 2.

**Expected Result:**
Five yes/no answers, each with one supporting sentence of real evidence, saved in the shared document — every "no" names what's actually missing, and every "yes" points to something specific you checked, not an assumption.

**Troubleshooting:**
- **Answered all five "yes" without much evidence** → Go back and write the specific evidence for each. A checklist answered with no evidence behind it doesn't actually confirm anything.
- No other common pitfalls noted for this exercise.

## Module 2: AI-Assisted Coding, Testing & Data Privacy

### Exercise 1: Generate and refactor a capstone feature's code with an AI assistant
**Objective:**
By the end of this exercise, you will have used your AI coding assistant to either generate one small, well-defined piece of your capstone from a clear description, or refactor an existing piece toward one named goal — never an open-ended "improve this" — and read every line before accepting it.

**Prerequisites for this exercise:**
An AI coding assistant connected to your editor, and your capstone's actual codebase open.

**Steps:**
1. Pick one small, well-defined piece of your capstone to work on — a single function or component, not a whole feature.
2. Decide whether you're generating new code or refactoring existing code in this exercise.
3. If generating, write a clear description of what the code should do, including its inputs, outputs, and one concrete example — not just a function name — and give that description to your AI coding assistant.
4. If refactoring, pick exactly one named goal for the refactor — for example "improve readability" or "remove duplication" — and give your assistant the existing code plus that one goal, not an open-ended "improve this."
5. Read the assistant's full output before accepting any of it.
6. Save the accepted code into your capstone's actual codebase.

**Expected Result:**
One small, well-defined piece of your capstone's code exists — either newly generated from a clear description, or refactored toward the one goal you named — and you read every line of it before it went in.

**Troubleshooting:**
- **Gave the assistant an open-ended "improve this" instead of one named goal** → Stop, pick one specific goal, and re-run the refactor. An unnamed goal makes it impossible to tell afterward whether the refactor actually succeeded.
- No other common pitfalls noted for this exercise.

### Exercise 2: Generate a unit test for that feature with the assistant, then run it
**Objective:**
By the end of this exercise, you will have generated a unit test for the Exercise 1 code with your AI assistant, and confirmed it passes against the current, working version of that code.

**Prerequisites for this exercise:**
The code from Module 2, Exercise 1 must exist.

**Steps:**
1. Ask your AI coding assistant to generate a unit test for the exact function or component you generated or refactored in Exercise 1.
2. Read the generated test in full before accepting it.
3. Save the test into your capstone's actual test suite.
4. Run your capstone's test suite, or just this one test, and confirm it passes against the current, working code.

**Expected Result:**
A saved test exists for the Exercise 1 code, and it passes when run against the current, working version of that code.

**Troubleshooting:**
- **Test passes but doesn't seem to check anything meaningful** — for example, it only confirms the function runs without erroring → Reread its assertions. If the test would still pass against wrong output, it isn't testing the behavior it claims to; ask the assistant to strengthen the assertions before moving on.
- No other common pitfalls noted for this exercise.

### Exercise 3: Review the AI-generated diff and fix one issue before it merges
**Objective:**
By the end of this exercise, you will have reviewed the Exercise 1 diff like a teammate's pull request, fixed one real issue in it, and directly proven the Exercise 2 test is meaningful by deliberately breaking the code and watching the test fail, then reverting.

**Prerequisites for this exercise:**
The code from Module 2, Exercise 1 and the test from Module 2, Exercise 2 must both exist, and the test must currently pass.

**Steps:**
1. Open the full diff of the code you generated or refactored in Exercise 1, as if reviewing a teammate's pull request rather than your own.
2. Read it line by line and find one real issue — a missed edge case, an inconsistent name, or a stale comment.
3. Fix that one issue directly in the code.
4. Run the Exercise 2 test again and confirm it still passes after your fix.
5. Temporarily break the Exercise 1 code on purpose — for example, flip a comparison operator or hardcode a wrong return value.
6. Run the Exercise 2 test again and confirm it now fails.
7. Revert your deliberate break from step 5, restoring the working, fixed code.
8. Run the test one final time and confirm it passes again.

**Expected Result:**
You found and fixed one real issue in the AI-generated code, and you've directly confirmed the Exercise 2 test is meaningful: it fails against deliberately broken code (steps 5–6) and passes again against the real, fixed code (steps 7–8).

**Troubleshooting:**
- **Broke the code in step 5 but the test still passed** → This is exactly the risk this exercise exists to catch: a test that passes against both correct and broken code isn't testing the behavior it claims to. Go back to Exercise 2 and ask your assistant to write an assertion that actually checks the specific behavior you broke.
- **Couldn't find a real issue in step 2** → Reread more slowly for a missed edge case, an inconsistent name, or a stale comment — "compiles and looks clean" is not the same as "was reviewed." If genuinely nothing is wrong, note that explicitly rather than skipping the review.

### Exercise 4: Write a data-handling note: what can and cannot go to a third-party AI tool
**Objective:**
By the end of this exercise, you will have a saved note listing two or three real categories of your capstone's own data, each marked plainly as safe or not safe to paste into an AI assistant's chat window, with a real reason for both.

**Prerequisites for this exercise:**
None beyond the course prerequisites.

**Steps:**
1. As a team, list two or three real categories of data your capstone actually handles — for example, customer ticket text, production credentials, internal architecture details.
2. For each category, state plainly: can this be pasted into an AI coding assistant's or model chat window — yes or no.
3. For each "yes," write one sentence naming the vendor policy that makes it acceptable — for example, OpenAI's "by default, we do not train on any inputs or outputs… including… the API," or Anthropic's "retained data is never used for model training without your express permission."
4. For each "no," write one sentence naming the actual risk if it were sent — for example, a production credential reaching a third party regardless of that vendor's training policy.
5. Add one closing sentence making explicit that a vendor not training on the data is a separate fact from whether the data should have been sent at all — that second call is the team's own.
6. Save the note in the same shared document as Module 1's exercises.

**Expected Result:**
A saved note listing two or three real capstone data categories, each with a clear yes/no on pasting it into an AI chat window, a one-sentence reason grounded in either vendor policy or real risk, and a closing sentence distinguishing "the vendor didn't train on it" from "it was fine to send."

**Troubleshooting:**
- **Marked something "yes" just because the vendor doesn't train on it** → Re-read step 5 — a vendor's training policy doesn't decide whether the data should have left the building at all. Production credentials and customer PII should typically be "no" regardless of vendor policy.
- No other common pitfalls noted for this exercise.
