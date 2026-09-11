"""
EXERCISE 12 — The same agent, rebuilt with LangChain's prebuilt create_agent

*** Core-adjacent enrichment: directly named in the Day 17 course-outline
content's own Assumption 1, not part of the six graded hands-on lines, but
not an outside addition either (unlike exercises 08-11's bonus patterns). ***

CONCEPT
-------
Exercises 01-07 built today's agent by hand, on purpose: `create_agent`'s
own loop, once called, is a black box - a team gets `agent.invoke(...)` and
a final answer, with the actual step-by-step routing (does the model's last
response contain a tool call, or not) hidden inside the library. Building
it by hand made that routing decision code you wrote and can read back.

`create_agent` itself was never meant to be skipped, though - just
deferred until the mechanism it wraps had already been built and watched
running. Confirmed against LangChain's own current documentation,
`create_agent` describes its own core loop exactly the way exercise 02's
`AgentState` + `call_model` + `tools_condition` + backward-edge loop
behaves: "an agent is a model calling tools in a loop until a given task is
complete." This exercise rebuilds exercises 02 and 04's agent - the loop
AND the bounded-step stopping condition - using `create_agent` directly,
so you can compare the hand-built version against the pre-built one on the
exact same task, having already built the thing being wrapped.

`create_agent`'s current middleware stack also covers exercise 04's
step bound and exercise 06's retry step as configurable, pre-built pieces:
`ModelCallLimitMiddleware` / `ToolCallLimitMiddleware` (a bound on model or
tool calls, with an `exit_behavior` choice between a graceful stop and a
hard error - the same "clean stop vs. crash" distinction exercise 04 drew
by hand) and `ToolRetryMiddleware` (a configurable `max_retries`, default
2, with real exponential backoff - the production version of exercise 06's
two-attempt wrapper). A different middleware worth knowing about, not
built here: `HumanInTheLoopMiddleware`, which pauses a run BEFORE a
specific tool executes and waits for a person to approve, edit, or reject
it - relevant the moment a tool takes a real, consequential action (for
example, Meridian Resorts & Spa's own Sprint 3 agent task: "stopping to
ask for confirmation before finalizing" a booked spa slot), a materially
different mechanism from a bounded loop and out of today's hands-on scope.

RUNNING SCENARIO
-----------------
The exact same two tools and the exact same test messages from exercises
02-04, run through `create_agent` instead of a hand-built `StateGraph`, to
compare behavior and code volume directly against something you already
built and understand.

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the same two tools as prior exercises. Nothing to change here.
# =============================================================================

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
EMBEDDING_MODEL = "text-embedding-3-small"
MAX_STEPS = 5  # same bound as exercise 04, for a fair comparison

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
    collection_name="day08_ex12_hospitality_docs",
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

TWO_TOOL_MESSAGE = "Can I get late checkout, and what does my reservation 214 say about check-out time?"
OPEN_ENDED_MESSAGE = "Tell me everything about my stay - reservation 214, pet policy, checkout, cancellation, spa, and Wi-Fi."

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given. Confirm each class/parameter name against LangChain's current
# documentation before you rely on it - this is exactly the kind of
# fast-moving surface the course content's own Step 8 review flags.
# =============================================================================

# STEP 0 — imports:
#   from langchain.agents import create_agent
#   from langchain.agents.middleware import ModelCallLimitMiddleware, ToolRetryMiddleware
# YOUR CODE HERE


# STEP 1 — build a bounded-step, retry-equipped agent with ONE
# create_agent(...) call: pass `model` (the plain, un-bound model from
# GIVEN - create_agent does its own tool binding internally), `tools`, and a
# `middleware` list containing a ModelCallLimitMiddleware configured with
# the same MAX_STEPS bound as exercise 04 and a graceful exit_behavior, plus
# a ToolRetryMiddleware configured with the same max_attempts as exercise
# 06's hand-written retry wrapper.
# YOUR CODE HERE


# STEP 2 — invoke your create_agent-built agent with TWO_TOOL_MESSAGE
# (wrapped as {"messages": [HumanMessage(content=...)]} - same input shape
# as exercise 02's hand-built graph) and print the final answer.
# YOUR CODE HERE


# STEP 3 — invoke it again with OPEN_ENDED_MESSAGE, and confirm it stops
# gracefully once your configured step bound is hit, the same behavior
# exercise 04 built and tested by hand - but built here in a fraction of
# the code.
# YOUR CODE HERE


# STEP 4 — write a short comment block comparing the two versions directly,
# from your own experience building both:
#   (a) how many lines of your own code did the create_agent version need,
#       versus exercises 02 + 04 + 06 combined?
#   (b) what can you SEE and step through in exercises 02/04/06's version
#       that create_agent's single call hides from you?
#   (c) if you were shipping this for a real Sprint 3 feature today, which
#       version would you actually choose, and why - is "less code" or
#       "full visibility into every decision" the more important property
#       for your team's specific agent task?
# YOUR ANSWERS HERE (as comments)


# EXPECTED RESULT
# ----------------
# Both versions should produce equivalent final answers on TWO_TOOL_MESSAGE
# and equivalent graceful (not crashing) stops on OPEN_ENDED_MESSAGE once
# their step bounds are hit - the same underlying loop mechanism, verified
# now from both the inside (exercises 02/04/06, built by hand) and the
# outside (this exercise, calling the pre-built version).
#
# Common Pitfalls:
# - Treating this exercise as proof the hand-built exercises "weren't
#   necessary" - the opposite is closer to true: understanding what
#   ModelCallLimitMiddleware and ToolRetryMiddleware are actually DOING
#   internally, well enough to configure them correctly and debug them
#   when they misbehave, is exactly what exercises 02, 04, and 06 bought you.
# - Assuming middleware class names, parameter names, and default values are
#   stable indefinitely - this is a fast-moving part of LangChain's surface;
#   re-confirm against LangChain's own current documentation close to
#   whenever you actually use this in a real project.
#
# What this demonstrates:
# The same "primitives first, current high-level wrapper named once the
# underlying shape is understood" sequencing this program has used since
# Day 15's LCEL-vs-StateGraph choice (see also day07/07_lcel_rag_chain.py's
# own README note), now completed at the agent level: `create_agent` is not
# a different idea from exercises 02-07's loop, it's the same idea, with the
# routing decision, the step bound, and the retry step all still happening -
# just no longer code you wrote yourself.
"""
Sources:
- LangChain: Agents overview — https://docs.langchain.com/oss/python/langchain/agents
- LangChain: Prebuilt middleware — https://docs.langchain.com/oss/python/langchain/middleware/built-in
- LangChain: Human-in-the-loop — https://docs.langchain.com/oss/python/langchain/human-in-the-loop
"""
