"""
BONUS EXERCISE 09 — Parallelization: fan-out/fan-in instead of ThreadPoolExecutor

*** This is enrichment, beyond today's graded outline (exercises 01-07). ***
Not covered elsewhere in this course - see the README's "Bonus: agentic
workflow patterns" section for why it's included and cited from.

CONCEPT
-------
Confirmed directly against LangGraph's own current documentation ("Workflows
and agents"), PARALLELIZATION is a named LangGraph pattern with a concrete
graph shape: multiple edges leave the SAME predecessor toward independent
nodes, and an "aggregator" node collects their results once all of them
finish - LangGraph's own reference example wires three nodes directly from
START, each into one aggregator. This isn't just a description of what
happens to run - it's how the LangGraph runtime schedules work: nodes that
share a predecessor and don't depend on each other's output belong to the
same "superstep," and LangGraph's own runtime documentation states plainly
that a superstep's job is to "execute all selected actors in parallel,
until all complete, or one fails, or a timeout is reached." The graph's
EDGE TOPOLOGY is what creates the parallelism - not a manually-managed
thread pool.

Exercise 02's decision loop calls its two tools SEQUENTIALLY, one after
another, because the model only ever learns it needs a second tool AFTER
seeing the first tool's result - that sequencing is correct and necessary
there. But look again at exercise 01's AMBIGUOUS_MESSAGE: "Can I get late
checkout, and what does my reservation say about check-out time?" Once it's
already decided - from the message alone - that it needs BOTH
get_reservation and answer_guest_question, and neither tool's result
depends on the other's, there's no reason to make the SAME node visit both
tools one after another. This exercise builds that case as two genuinely
separate LangGraph nodes, fanned out from START, so the runtime itself runs
them concurrently - the same message content invoked against two different
graphs (one wired to fan out, one wired sequentially) to make the resulting
timing difference measurable, not just asserted.

RUNNING SCENARIO
-----------------
The same two tools from exercises 01-07, each wrapped as its own graph node
with an artificial delay so the timing difference in Step 5 is actually
visible (a real network-bound tool call already has this kind of latency;
the delay here just makes it reproducible in a classroom setting) - built
into two small graphs with the SAME two nodes, wired two different ways.

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the same two tools as prior exercises, each wrapped with an
# artificial delay so the timing difference in Step 5 is actually visible.
# Nothing to change here.
# =============================================================================

import time
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model

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
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
# YOUR CODE HERE


# STEP 1 — define ParallelState, a TypedDict with four fields:
# reservation_id (str), policy_question (str), reservation_result (str),
# and policy_result (str).
# YOUR CODE HERE


# STEP 2 — write two node functions:
#   - call_get_reservation(state) -> dict: return
#     {"reservation_result": get_reservation_raw(state["reservation_id"])}
#   - call_answer_question(state) -> dict: return
#     {"policy_result": answer_guest_question_raw(state["policy_question"])}
def call_get_reservation(state) -> dict:
    # YOUR CODE HERE
    pass

def call_answer_question(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 3 — build build_parallel_graph(), a function with no arguments that
# returns a COMPILED graph:
#   - builder = StateGraph(ParallelState)
#   - add both node functions from Step 2, naming them "get_reservation"
#     and "answer_question"
#   - add TWO edges from START: one to "get_reservation", one to
#     "answer_question" - this is the fan-out that makes them run in the
#     same superstep, concurrently
#   - add an edge from EACH of the two nodes directly to END (no aggregator
#     node needed yet - Step 4 explains why)
#   - return builder.compile()
def build_parallel_graph():
    # YOUR CODE HERE
    pass


# STEP 4 — build build_sequential_graph(), the SAME two nodes, wired
# differently, to serve as this exercise's timing baseline:
#   - builder = StateGraph(ParallelState)
#   - add the SAME two node functions, same names
#   - wire them in a straight line instead of a fan-out: START ->
#     "get_reservation" -> "answer_question" -> END
#   - return builder.compile()
# (Notice both graphs share the exact same node functions - only the EDGE
# TOPOLOGY differs. That's the entire point: parallelism here is a property
# of how the graph is wired, not of the node functions themselves.)
def build_sequential_graph():
    # YOUR CODE HERE
    pass


# STEP 5 — write run_and_time(graph) -> tuple[dict, float]:
#   - record a start time
#   - call graph.invoke({"reservation_id": RESERVATION_ID, "policy_question": POLICY_QUESTION})
#   - record the elapsed time (end - start)
#   - return (final_state, elapsed_seconds)
def run_and_time(graph):
    # YOUR CODE HERE
    pass


# STEP 6 — call run_and_time on build_sequential_graph() and on
# build_parallel_graph(), printing each result's reservation_result,
# policy_result, and elapsed time, then print a final comparison line
# showing the speedup (sequential_time / parallel_time).
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# Both graphs should return the SAME reservation_result and policy_result
# (correctness is unaffected by edge topology). The sequential graph's
# elapsed time should be roughly the SUM of both calls' delays
# (~2x ARTIFICIAL_DELAY_SECONDS plus real API latency); the parallel
# graph's elapsed time should be roughly the delay of the SLOWER of the
# two calls alone (~1x ARTIFICIAL_DELAY_SECONDS plus that call's own real
# API latency) - a measurable, printed speedup, produced by LangGraph's own
# same-superstep scheduling, with no thread-pool code written by hand.
#
# Common Pitfalls:
# - Wiring build_parallel_graph() with an edge from "get_reservation" to
#   "answer_question" (instead of two separate edges from START) by
#   habit - that silently turns the "parallel" graph back into the
#   sequential one, despite having the exact same node set.
# - Expecting an EXACT ARTIFICIAL_DELAY_SECONDS reading from either
#   graph - real embeddings and chat-completion calls inside
#   answer_guest_question_raw add real network latency on top of the
#   artificial sleep, so both numbers run a bit higher than the raw
#   multiplier; what matters is the RATIO between the two, not hitting an
#   exact number.
# - Applying this pattern to two nodes that AREN'T actually independent
#   (for example, if a real second lookup needed the first lookup's result
#   as an input) - parallelization is only valid for genuinely independent
#   work; exercise 02's loop stays sequential specifically because it
#   doesn't know it needs the second tool until it's seen the first tool's
#   result.
"""
Sources:
- LangGraph: Workflows and agents (Parallelization) — https://docs.langchain.com/oss/python/langgraph/workflows-agents
- LangGraph runtime (superstep execution) — https://docs.langchain.com/oss/python/langgraph/pregel
"""
