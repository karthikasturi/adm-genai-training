"""
BONUS EXERCISE 13 — The same territory, one tier higher: LangChain's Deep Agents

*** This goes BEYOND the course outline's own explicit scope, further than
exercises 08-11 and 12 do. Read the SCOPE NOTE below before writing any code. ***

SCOPE NOTE - read this first
-------------------------------
The Day 17 course content's own Landscape anchor names LangChain's current
three-tier stack directly: LangGraph (the primitives exercises 01-07 build
by hand), `create_agent` (the configurable mid-level harness exercise 12
builds), and Deep Agents (a "batteries-included," highest-level option).
That same content is explicit that Deep Agents "stays outside today's scope
entirely... worth naming to the room only as the next tier up... never
built against." Exercise 12 was still inside the outline's own stated
intent (Assumption 1 explicitly commits to building `create_agent` once the
hand-built loop exists). This exercise is not - it's genuinely outside what
Day 17's own content calls for, built here because it was specifically
asked for, not because the outline asks for it. Treat it as a look at where
LangChain's own stack goes NEXT, past today's actual graded scope, not as
something today's Sprint 3 deliverable needs.

CONCEPT
-------
Confirmed directly against LangChain's own current documentation and
reference pages, Deep Agents is an "agent harness" built on top of
LangGraph's runtime, offering several capabilities NONE of exercises 01-12
have: a virtual filesystem (`ls`, `read_file`, `write_file`, `edit_file`,
`glob`, `grep`, backed by agent state by default - not real disk), a
task-planning tool (`write_todos`, via middleware), and genuine SUBAGENT
DELEGATION - a built-in `task` tool that hands a self-contained piece of
work to a separately-configured subagent (its own system prompt, its own
tool subset, even its own model) and returns only that subagent's finished
result to the main agent's context.

That last capability is the one worth sitting with, because it's a
different SHAPE of work-splitting than anything built so far. Exercise 11's
orchestrator-workers pattern already decomposed a task into subtasks and
delegated each to a worker CALL - but every worker there was a single,
non-looping LLM call answering one sub-question. A Deep Agents subagent, by
contrast, is itself a small tool-calling agent, capable of its own multi-
step reasoning and its own tool use, before it ever reports back - genuine
task delegation to a bounded agent, not just a parallel LLM call. This is
also precisely why Deep Agents' value only shows up on a task that's
actually big enough to need it: a two-tool, few-step task (exercises 01-07's
own scenario) gets no real benefit from planning or delegation it doesn't
need - which is exactly why this exercise uses a deliberately LARGER task
than exercises 01-12 did.

RUNNING SCENARIO
-----------------
Drafting a full pre-arrival welcome packet for a guest - a genuinely
multi-part document (confirmed reservation details, answers to several
different policy questions, and a written summary), assembled by a Deep
Agent that plans its own steps, delegates the policy research to a
dedicated subagent, and writes the finished packet to a file via its own
built-in filesystem tools.
# [Placeholder — replace with a genuinely multi-step, multi-part task from
# your own Sprint 3 agent brief - something too large for a fixed two-tool
# loop to feel like the natural fit]

SETUP
-----
    pip install deepagents langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
(deepagents is the one genuinely NEW package this whole lab set installs -
everything in exercises 01-12 needed nothing beyond what Days 15-16 already
had. Confirm the exact current API against
https://reference.langchain.com/python/deepagents before relying on any
parameter name below - this is an actively developing package.)
"""

# =============================================================================
# GIVEN — the same two tools as prior exercises, reused unchanged as the
# Deep Agent's own custom tools (on top of its built-in filesystem and
# task-delegation tools, which need no setup). Nothing to change here.
# =============================================================================

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>" - passed
                                     # to create_deep_agent as a plain string,
                                     # same provider:model shape used everywhere
                                     # else in this course
EMBEDDING_MODEL = "text-embedding-3-small"

model = init_chat_model(CHAT_MODEL)

SAMPLE_RESERVATIONS = {
    "214": "check_in=2026-09-20, status=confirmed, room_type=Deluxe King",
    "310": "check_in=2026-09-25, status=pending, room_type=Standard Queen",
}

@tool
def get_reservation(reservation_id: str) -> str:
    """Look up a reservation by ID and return its check-in date, status, and room type.

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
    collection_name="day08_ex13_hospitality_docs",
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

# A deliberately multi-part task - too large to fit exercises 01-07's
# two-tool, few-step scenario comfortably, and genuinely benefiting from
# planning and delegation rather than just a longer sequential loop.
WELCOME_PACKET_TASK = (
    "Draft a pre-arrival welcome packet for reservation 214. Confirm the "
    "reservation's check-in date, status, and room type. Then answer these "
    "guest questions using the property's reference documents: can they "
    "bring a pet to dinner, what are the spa hours, and how does Wi-Fi "
    "access work. Write the finished packet, with a short friendly intro "
    "and one section per topic, to a file named "
    "'guest_214_welcome_packet.md'."
)

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given. Confirm every parameter name against deepagents' current
# reference documentation first - see the SETUP note above.
# =============================================================================

# STEP 0 — imports:
#   from deepagents import create_deep_agent
# YOUR CODE HERE
from deepagents import create_deep_agent, SubAgent


# STEP 1 — build a Deep Agent with ONE create_deep_agent(...) call:
#   - model: CHAT_MODEL
#   - tools: [get_reservation, answer_guest_question] - your two existing
#     tools, merged additively alongside Deep Agents' own built-in
#     filesystem and delegation tools (nothing about them needs re-declaring)
#   - system_prompt: a short instruction naming the hotel assistant's job
#     and telling it to write its final output to the requested file using
#     its own write_file tool, not just returning the packet as chat text
# YOUR CODE HERE
agent = create_deep_agent(
    model=CHAT_MODEL,
    tools=[get_reservation, answer_guest_question],
    system_prompt=(
        "You are a hotel assistant. Write the final welcome packet to the "
        "requested file using your write_file tool."
    )
)

# STEP 2 — invoke your Deep Agent with WELCOME_PACKET_TASK (the input shape
# is {"messages": [...]} , same as every prior exercise's compiled graph -
# a plain string task description or a HumanMessage both work). Print the
# full response.
# YOUR CODE HERE
message_input= {"messages": [WELCOME_PACKET_TASK]}

# response = agent.invoke(message_input)
# print(response["messages"][-1].content) 

# STEP 3 — read back the file the agent should have written. Deep Agents'
# default backend keeps its virtual filesystem IN THE AGENT'S OWN RETURNED
# STATE, not on real disk - inspect the invoke result's "files" key (or
# call the agent's own read_file tool again in a follow-up message asking
# it to show you the file's contents) rather than looking for a real file
# on your machine. Print the packet's contents once you've found them.
# YOUR CODE HERE
# print(response["files"]["guest_214_welcome_packet.md"])

# STEP 4 — add ONE subagent and confirm real delegation happens. Rebuild
# your agent (Step 1) with a `subagents` argument: a list containing one
# subagent definition naming a "policy-researcher" (a short description of
# its job, a system_prompt telling it to use answer_guest_question and
# report findings concisely, and tools=[answer_guest_question]) - check
# deepagents' current reference for whether your installed version expects
# a SubAgent object (from deepagents import SubAgent) or an equivalently-
# shaped plain dict. Re-run Step 2 and look for evidence in the printed
# output (or in a streamed run, if you try agent.stream(...) instead) that
# the main agent actually called its built-in `task` tool to hand the
# policy questions to this subagent, rather than answering them itself.
# YOUR CODE HERE
subagent = SubAgent(
    name="policy-researcher",
    description="Researches hotel policies and answers guest questions concisely.",
    system_prompt=(
        "You are a policy researcher. Use the answer_guest_question tool to "
        "find accurate answers and report your findings concisely."
    ),
    tools=[answer_guest_question]
)

agent = create_deep_agent(
    model=CHAT_MODEL,
    tools=[get_reservation, answer_guest_question],
    system_prompt=(
        "You are a hotel assistant. Write the final welcome packet to the "
        "requested file using your write_file tool."
    ),
    subagents=[subagent]
)

response = agent.invoke(message_input)
print(response["messages"][-1].content)
print(response["files"]["/guest_214_welcome_packet.md"])


# EXPECTED RESULT
# ----------------
# A finished welcome packet, written via the agent's own write_file tool
# (not code you wrote to save a file), containing a short intro plus one
# section per topic (reservation details, pet policy, spa hours, Wi-Fi),
# with each policy answer actually grounded in your CHUNKS documents rather
# than guessed. With Step 4's subagent added, the printed/streamed trace
# should show a `task` tool call handing the policy questions off, distinct
# from the main agent calling answer_guest_question directly itself.
#
# Common Pitfalls:
# - Looking for guest_214_welcome_packet.md on your real filesystem - Deep
#   Agents' default backend is a VIRTUAL, state-backed filesystem, not real
#   disk. A file that only exists in the agent's own returned state is
#   still a real, working result for this exercise; confirm you're reading
#   it from the right place before assuming the task failed.
# - Treating this exercise's bigger task as proof Deep Agents is simply
#   "better" than exercises 01-07's hand-built loop - the comparison isn't
#   fair in that direction: exercises 01-07's task was deliberately small
#   enough that a hand-built two-tool loop was already the right size for
#   it. Reach for Deep Agents when the task itself is genuinely large
#   enough to need planning and delegation, the same conditional framing
#   exercise 11's own common pitfalls note made for orchestrator-workers.
# - Assuming every parameter name above is stable - deepagents is an
#   actively developing package; re-confirm signatures close to whenever
#   you actually rely on this.
#
# What this demonstrates:
# This completes the climb Day 15's own Landscape anchor first laid out:
# LangGraph primitives (exercises 01-07) → create_agent (exercise 12) →
# Deep Agents (this exercise) - the same underlying "a model calling tools
# in a loop" idea, each tier trading away a little visibility for a lot
# more built-in capability. Exercise 12's own closing question ("is 'less
# code' or 'full visibility' the more important property for your team's
# task?") gets a third data point here: Deep Agents trades away even MORE
# visibility than create_agent did, in exchange for planning and
# delegation neither of the lower two tiers offer at all.
"""
Sources:
- LangChain: Deep Agents overview — https://docs.langchain.com/oss/python/deepagents/overview
- create_deep_agent reference — https://reference.langchain.com/python/deepagents/graph/create_deep_agent
- deepagents (GitHub) — https://github.com/langchain-ai/deepagents
"""
