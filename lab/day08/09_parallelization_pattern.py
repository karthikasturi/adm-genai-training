"""
BONUS EXERCISE 09 — Parallelization: running independent tool calls concurrently

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section for why it's included and cited from.

CONCEPT
-------
Anthropic's "Building Effective Agents" names PARALLELIZATION as a workflow
pattern with two variations: SECTIONING (breaking one task into independent
subtasks run at the same time) and VOTING (running the identical task
multiple times for a consensus answer). Exercise 02's decision loop calls
its two tools SEQUENTIALLY, one after another, because the model only ever
learns it needs a second tool AFTER seeing the first tool's result - that
sequencing is correct and necessary there.

But look again at exercise 01's AMBIGUOUS_MESSAGE: "Can I get late
checkout, and what does my reservation say about check-out time?" Once the
model has ALREADY decided, from the message alone, that it needs BOTH
get_reservation and answer_guest_question - and neither tool's result
depends on the other's - there's no reason to wait for one to finish before
starting the other. This exercise builds that SECTIONING case directly:
given a message that needs two genuinely independent lookups, run both
tool calls CONCURRENTLY instead of sequentially, and confirm the wall-clock
time actually drops.

RUNNING SCENARIO
-----------------
The same two tools from exercises 01-07, called directly (not through the
agent loop) with two independent, deliberately-slowed-down calls - first
timed sequentially, then timed concurrently - to make the difference
measurable, not just asserted.

SETUP
-----
    pip install langchain langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the same two tools as prior exercises, each wrapped with an
# artificial delay so the timing difference in Step 3 is actually visible
# (a real network-bound tool call already has this kind of latency; the
# delay here just makes it reproducible in a classroom setting). Nothing to
# change here.
# =============================================================================

import time
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
EMBEDDING_MODEL = "text-embedding-3-small"
ARTIFICIAL_DELAY_SECONDS = 1.5  # stands in for real network latency

model = init_chat_model(CHAT_MODEL)

SAMPLE_RESERVATIONS = {
    "214": "check_in=2026-09-20, status=confirmed",
    "310": "check_in=2026-09-25, status=pending",
}

def get_reservation_raw(reservation_id: str) -> str:
    time.sleep(ARTIFICIAL_DELAY_SECONDS)
    return SAMPLE_RESERVATIONS.get(reservation_id, "no reservation found with that ID")

CHUNKS = [
    "Pet Policy: Guests are welcome to bring pets to all outdoor dining areas and to designated pet-friendly rooms on the ground floor. A one-time pet fee of 35 USD applies per stay.",
    "Checkout Policy: Standard checkout time is 11:00 AM. Late checkout until 1:00 PM may be arranged with the front desk at no charge, subject to availability.",
    "Cancellation Policy: Cancellations made more than 48 hours before check-in receive a full refund. Cancellations made within 48 hours are charged for one night's stay.",
    "Spa Hours: The spa is open daily from 8:00 AM to 9:00 PM. A 24-hour cancellation notice is required to avoid a fee equal to 50 percent of the treatment price.",
    "Wi-Fi Access: Wi-Fi is complimentary in all rooms and public areas. The network name and password are printed on the welcome card left in every room at check-in.",
]

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    collection_name="day08_ex09_hospitality_docs",
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"},
)
vectorstore.add_texts(CHUNKS)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

answer_prompt = PromptTemplate.from_template(
    "Answer the guest's question using ONLY the context below. "
    "If the context doesn't contain the answer, say you're not sure.\n\n"
    "Context:\n{context}\n\nGuest question: {question}"
)

def answer_guest_question_raw(question: str) -> str:
    time.sleep(ARTIFICIAL_DELAY_SECONDS)
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = answer_prompt.invoke({"context": context, "question": question})
    return model.invoke(prompt).content

# Two genuinely independent lookups - neither result depends on the other.
RESERVATION_ID = "214"
POLICY_QUESTION = "Can I bring my dog to the restaurant?"

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 0 — additional imports you'll need:
#   from concurrent.futures import ThreadPoolExecutor
# YOUR CODE HERE


# STEP 1 — write run_sequentially() -> tuple[str, str, float]:
#   - record a start time
#   - call get_reservation_raw(RESERVATION_ID), then
#     answer_guest_question_raw(POLICY_QUESTION), one after the other
#   - record the elapsed time (end - start)
#   - return (reservation_result, policy_result, elapsed_seconds)
def run_sequentially():
    # YOUR CODE HERE
    pass


# STEP 2 — write run_in_parallel() -> tuple[str, str, float]:
#   - record a start time
#   - using a ThreadPoolExecutor (max_workers=2), submit BOTH
#     get_reservation_raw(RESERVATION_ID) and
#     answer_guest_question_raw(POLICY_QUESTION) so they run concurrently,
#     then call .result() on each future to collect both outputs
#   - record the elapsed time
#   - return (reservation_result, policy_result, elapsed_seconds)
def run_in_parallel():
    # YOUR CODE HERE
    pass


# STEP 3 — call both functions, printing each one's two results and its
# elapsed time, and print a final comparison line showing the speedup
# (sequential_time / parallel_time).
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# Both functions should return the SAME two results (correctness is
# unaffected by ordering). run_sequentially's elapsed time should be
# roughly the SUM of both calls' delays (~2x ARTIFICIAL_DELAY_SECONDS);
# run_in_parallel's elapsed time should be roughly the delay of the SLOWER
# of the two calls alone (~1x ARTIFICIAL_DELAY_SECONDS) - a measurable,
# printed speedup, not just an assertion that concurrency "should" help.
#
# Common Pitfalls:
# - Calling .result() on a future immediately after .submit() for that same
#   future, before submitting the second one - that blocks on the first
#   call before the second ever starts, silently turning "parallel" back
#   into "sequential." Submit BOTH first, THEN call .result() on each.
# - Applying this pattern to two calls that AREN'T actually independent (for
#   example, if a real second lookup needed the first lookup's result as an
#   input) - parallelization is only valid for genuinely independent work;
#   exercise 02's loop stays sequential specifically because it doesn't
#   know it needs the second tool until it's seen the first tool's result.
"""
Sources:
- Anthropic: Building Effective Agents — https://www.anthropic.com/engineering/building-effective-agents
"""
