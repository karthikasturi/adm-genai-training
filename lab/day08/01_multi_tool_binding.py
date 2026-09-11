"""
EXERCISE 01 — Multi-tool binding: giving the model more than one real option

CONCEPT
-------
Day 15's chain routing function was deliberately dumb, in the best sense: a
few lines of Python, checking one field, returning one of two known
strings - exactly right for a decision that's fully knowable in advance.
Consider The Aldwyn House's own Sprint 3 concierge task: "interpret a
guest's free-text request..., check eligibility against the reservation
record, and create/update a ConciergeRequest." A guest's message might need
one lookup, or several, depending on what the first one returns - the
NUMBER of steps isn't knowable in advance the way a fixed routing function
needs it to be. That's a job for an AGENT: instead of a human-authored
routing function deciding the next step, the model itself looks at the
task so far and chooses one of two things - call one specific tool with
specific arguments, or produce a final answer because the task is done.
LangChain's own documentation frames this as "Agent = Model + Harness": the
model supplies the judgment, the harness (the prompt, the tools, any
middleware) is the surrounding structure that makes that judgment safe to
call repeatedly.

Mechanically, nothing about HOW a model chooses a tool is new - it's the
same bind_tools([...]) mechanism Day 15's tool-integration exercise
(lab/day06/05_tool_integration.py) already used. What's new here is that
TWO tools are bound at once instead of one, so there's a real choice to
observe before this exercise set builds the actual loop (exercise 02) that
lets the model act on that choice repeatedly.

RUNNING SCENARIO
-----------------
The same hospitality assistant from Days 15-16, now with BOTH of its
previously-built tools available at once: Module 15B's get_reservation and
Module 16B's answer_guest_question, reused exactly as each was already
built and verified - not rebuilt here. This exercise only asks: given both
tools, which one does the model actually pick for a given message?
# [Placeholder — replace with your team's actual Sprint 3 agent task and its
# own two (or more) real tools]

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...      # embeddings, and optionally chat
    export ANTHROPIC_API_KEY=...   # optional, for the chat model instead
(No new package today - everything here was already installed for Days 15-16.)
"""

# =============================================================================
# GIVEN — Module 15B's get_reservation and Module 16B's answer_guest_question,
# reused exactly as built (this content's own Assumption 2: today's two tools
# are not reinvented). A plain, not-yet-tool-bound `model` is also provided -
# binding it to both tools is today's actual new work, below.
# =============================================================================

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
EMBEDDING_MODEL = "text-embedding-3-small"

model = init_chat_model(CHAT_MODEL)

# --- Tool 1: Module 15B's get_reservation, unchanged ---
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

# --- Tool 2: Module 16B's answer_guest_question, unchanged ---
CHUNKS = [
    "Pet Policy: Guests are welcome to bring pets to all outdoor dining areas and to designated pet-friendly rooms on the ground floor. A one-time pet fee of 35 USD applies per stay.",
    "Checkout Policy: Standard checkout time is 11:00 AM. Late checkout until 1:00 PM may be arranged with the front desk at no charge, subject to availability.",
    "Cancellation Policy: Cancellations made more than 48 hours before check-in receive a full refund. Cancellations made within 48 hours are charged for one night's stay.",
    "Spa Hours: The spa is open daily from 8:00 AM to 9:00 PM. A 24-hour cancellation notice is required to avoid a fee equal to 50 percent of the treatment price.",
    "Wi-Fi Access: Wi-Fi is complimentary in all rooms and public areas. The network name and password are printed on the welcome card left in every room at check-in.",
]

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
vectorstore = Chroma(
    collection_name="day08_ex01_hospitality_docs",
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

# Three messages, deliberately covering three different tool-choice cases.
RESERVATION_ONLY_MESSAGE = "Can you check the status of reservation 214 for me?"
POLICY_ONLY_MESSAGE = "Can I bring my dog to the restaurant?"
AMBIGUOUS_MESSAGE = "Can I get late checkout, and what does my reservation say about check-out time?"

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 0 — additional imports you'll need beyond the GIVEN section's:
#   from langchain_core.messages import HumanMessage
# YOUR CODE HERE


# STEP 1 — bind BOTH tools to the plain `model` from GIVEN, in one list, with
# one bind_tools([...]) call (same mechanism as lab/day06/05_tool_integration.py,
# now with two tools instead of one):
#   tools = [get_reservation, answer_guest_question]
#   model_with_tools = model.bind_tools(tools)
# YOUR CODE HERE


# STEP 2 — write inspect_tool_choice(message: str) -> None that:
#   - wraps message in a HumanMessage and calls model_with_tools.invoke([...])
#   - prints the message itself
#   - prints response.tool_calls (a list - empty if the model chose to answer
#     directly with no tool call at all)
#   - for each entry in response.tool_calls, prints its "name" and "args"
#     keys, so you can see exactly which tool the model picked and with what
#     arguments
def inspect_tool_choice(message: str) -> None:
    # YOUR CODE HERE
    pass


# STEP 3 — call inspect_tool_choice once for each of RESERVATION_ONLY_MESSAGE,
# POLICY_ONLY_MESSAGE, and AMBIGUOUS_MESSAGE, printing a separator between
# each so the three results are easy to tell apart.
# YOUR CODE HERE


# EXPECTED BEHAVIOR ONCE IMPLEMENTED
# -----------------------------------
# RESERVATION_ONLY_MESSAGE should produce exactly one tool call, named
# "get_reservation". POLICY_ONLY_MESSAGE should produce exactly one tool
# call, named "answer_guest_question". AMBIGUOUS_MESSAGE is the interesting
# one: it genuinely needs BOTH tools, but a single model call only ever gets
# to request tools ONCE, based on the message as it stands right now - it
# has no way yet to see one tool's result before deciding about the second.
# That gap (not being able to act, look at what happened, and decide again)
# is exactly what exercise 02's decision loop exists to close.
#
# What this demonstrates:
# Binding two tools doesn't just make two things POSSIBLE to call - it hands
# the model a genuine choice it has to make correctly, using each tool's own
# docstring as its only guide. That choice, checked back in after every
# single action instead of made once up front, is the entire mechanical
# difference between yesterday's chain and today's agent - exercise 02
# builds the loop that lets the model make this choice more than once.
