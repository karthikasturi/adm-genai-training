"""
EXERCISE 07 — Capstone: run a test task and diagnose a real failure mode

CONCEPT
-------
With a bounded loop (exercise 04), correct tool choice (exercise 05), and a
retry step (exercise 06), today's agent has every piece the outline's own
objective names. What remains is not a new mechanism, but a discipline this
program has practiced in a different form every prior GenAI-focused day:
don't just build it and assume it works - run it against a case designed to
surface a real failure, and read what actually happened.

Two failure modes are named explicitly: a LOOP (the agent approaches its
step bound without a good reason to), or a WRONG TOOL CALL (exercise 05's
own risk, resurfacing on a harder message than the clearly-scoped test
cases already fixed). This exercise asks you to deliberately provoke one of
them, diagnose which one actually happened and WHY from your own printed
trace, fix the specific cause, and confirm the fix.

RUNNING SCENARIO
-----------------
Your own finished agent (exercises 02, 04, 05, and 06's pieces combined),
run against one adversarial test message your team designs, specifically
intended to surface a loop or a wrong tool call.
# [Placeholder — replace with an adversarial message drawn from your team's
# actual Sprint 3 agent task and its own tools]

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the same two tools as prior exercises. Nothing to change here.
# Combine exercise 04's step-bounded routing and exercise 06's retry-wrapped
# tool node into ONE finished agent below - both pieces already exist in
# your own prior files; this exercise asks you to assemble them together.
# =============================================================================

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
EMBEDDING_MODEL = "text-embedding-3-small"
MAX_STEPS = 5

model = init_chat_model(CHAT_MODEL)

SAMPLE_RESERVATIONS = {
    "214": "check_in=2026-09-20, status=confirmed",
    "310": "check_in=2026-09-25, status=pending",
}

@tool
def get_reservation(reservation_id: str) -> str:
    """Look up a reservation by ID and return its check-in date and status.

    Use this when a guest's request depends on the details of a specific, existing reservation rather than a general policy question.
    """
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
    collection_name="day08_ex07_hospitality_docs",
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

def rag_answer(question: str) -> str:
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    prompt = answer_prompt.invoke({"context": context, "question": question})
    return model.invoke(prompt).content

@tool
def answer_guest_question(question: str) -> str:
    """Answer a guest's question using the hotel's reference documents.

    Use this for any question about policies, amenities, hours, or
    other information found in the property's own documents.
    """
    return rag_answer(question)

tools = [get_reservation, answer_guest_question]
model_with_tools = model.bind_tools(tools)

# [Placeholder — replace with an adversarial message your team designs from
# your own Sprint 3 agent task: either ambiguous enough to push the agent
# toward looping longer than necessary, or worded to plausibly trigger the
# wrong tool.]
ADVERSARIAL_TEST_MESSAGE = "I have a question about my stay - can you sort it out for me?"

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 1 — define AgentState (messages + step_count, as in exercise 04).
# YOUR CODE HERE


# STEP 2 — write call_model(state) -> dict (as in exercise 04: invokes
# model_with_tools, prints the decision, increments step_count).
def call_model(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 3 — write route_with_step_limit(state) -> str (as in exercise 04:
# checks step_count against MAX_STEPS before deferring to tools_condition).
def route_with_step_limit(state) -> str:
    # YOUR CODE HERE
    pass


# STEP 4 — write call_tool_with_retry(tool, tool_call, max_attempts=2) -> str
# and tool_node_with_retry(state) -> dict (as in exercise 06), so this
# finished agent's tool-execution step also retries a failed call once
# before giving up.
def call_tool_with_retry(tool, tool_call, max_attempts: int = 2) -> str:
    # YOUR CODE HERE
    pass

def tool_node_with_retry(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 5 — build the finished graph combining every piece above: call_model,
# tool_node_with_retry (named "tools"), the conditional edge via
# route_with_step_limit, and the loop-closing edge. Compile into `agent`.
# YOUR CODE HERE


# STEP 6 — write your own ADVERSARIAL_TEST_MESSAGE above (in GIVEN) targeting
# a real failure mode from YOUR team's Sprint 3 agent task - either a message
# ambiguous enough to approach MAX_STEPS without a good reason, or one
# plausibly likely to trigger the wrong tool. Invoke `agent` with it
# (step_count: 0 in the initial state) and print the FULL message trace:
# every message's type, tool calls (if any), and content, in order.
# YOUR CODE HERE


# STEP 7 — DIAGNOSE: reading only your own Step 6 printed trace (not
# guessing), write a short comment block right here naming:
#   (a) which failure mode actually occurred - a loop, a wrong tool call, or
#       neither (the agent handled it correctly, in which case design a
#       harder test message and repeat Steps 6-7)
#   (b) the SPECIFIC cause - point to the exact docstring wording, the
#       ambiguous phrase in the test message, or the step-bound value
#       responsible, citing the trace line(s) that show it
# YOUR DIAGNOSIS HERE (as a comment)


# STEP 8 — FIX the specific cause you diagnosed in Step 7 (a clearer
# docstring, a different MAX_STEPS value, or - if the message itself was the
# problem - a note explaining what a real guest would need to say
# differently for a well-built agent to handle it correctly), then re-run
# Step 6 and confirm the same test message now resolves correctly.
# YOUR CODE HERE


# EXPECTED RESULT
# ----------------
# An agent that halts on task completion for a normal request, halts
# cleanly at a bounded step count instead of looping indefinitely or
# crashing, chooses the correct tool for clearly-scoped test messages,
# recovers transparently from one injected tool failure, and has been run
# against a deliberately adversarial test case whose specific failure mode
# you can name, explain from your own printed trace, and have since fixed.
#
# Common Pitfalls:
# - Declaring this exercise complete after simply running the test message
#   once and observing a wrong answer, without actually reading the printed
#   trace to identify WHICH failure mode occurred and WHY - "diagnose" means
#   pointing to the specific cause, not just noticing something went wrong.
# - Designing a test message so extreme it doesn't resemble anything a real
#   guest would actually type - the diagnostic value comes from a message
#   that's realistic AND adversarial, not a deliberately broken one.
# - Fixing the SYMPTOM (rewording the test message until it happens to pass)
#   instead of the actual CAUSE (the docstring, the step bound, or the
#   routing logic) - the fix should make the agent more robust to a family
#   of similar messages, not just this one exact string.
