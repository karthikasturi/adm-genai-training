"""
EXERCISE 02 — The decision loop: a conditional edge that points backward

CONCEPT
-------
Exercise 01 showed the model choosing a tool ONCE, from a fixed message.
Turning that single choice into an actual LOOP - call the model, act on its
decision, feed the result back, call the model again - is a graph problem
this room already has every primitive for, plus exactly one new idea.

Every StateGraph piece today's loop needs already exists: a typed state
(an AgentState carrying the running list of messages, using LangGraph's own
`add_messages` reducer so new messages APPEND instead of overwriting); a
node (a plain function - one that calls the model, one that executes
whichever tool the model asked for); and a conditional edge, using
LangGraph's own prebuilt `tools_condition` - "if the last AIMessage contains
tool calls, route to the tool execution node; otherwise, end the workflow."

The one genuinely NEW idea: instead of routing to two different nodes that
both lead to END (Day 15's branching shape), today's tool-execution node
has its own edge leading BACK to the model node - the same node just
visited - so after a tool runs, the model is called again, now able to see
that tool's result, and asked to decide again: call another tool, or
answer. That backward-pointing edge is the entire mechanical difference
between a chain and an agent.

This architecture - reason about what to do, act, read the result, reason
again - has a name and a real citable origin: ReAct (Reason + Act),
introduced in "ReAct: Synergizing Reasoning and Acting in Language Models"
(Yao et al., 2022). The paper's own finding: interleaving reasoning with
real actions works better than either alone, because reasoning traces help
track and update a plan while actions let the model gather new information
the reasoning alone couldn't have known.

RUNNING SCENARIO
-----------------
The same two tools from exercise 01, now wired into an actual loop, tested
against a message that plausibly needs both of them in sequence.
# [Placeholder — replace with a message drawn from your team's actual
# Sprint 3 agent task]

SETUP
-----
    pip install langchain langgraph langchain-openai langchain-chroma python-dotenv
    export OPENAI_API_KEY=...
    export ANTHROPIC_API_KEY=...   # optional
"""

# =============================================================================
# GIVEN — the same two tools as exercise 01, unchanged. Nothing to change here.
# =============================================================================

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage

CHAT_MODEL = "openai:gpt-5.4-mini"  # or "anthropic:<current-model>"
EMBEDDING_MODEL = "text-embedding-3-small"

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
    collection_name="day08_ex02_hospitality_docs",
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

# A message that plausibly needs BOTH tools, one after the other.
TWO_TOOL_MESSAGE = "Can I get late checkout, and what does my reservation 214 say about check-out time?"

# =============================================================================
# YOUR TURN — each numbered STEP below describes what to write. No solution
# code is filled in; write it yourself under the comment, using the exact
# names given.
# =============================================================================

# STEP 0 — imports you'll need beyond the GIVEN section's:
#   from typing import Annotated
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
#   from langgraph.graph.message import add_messages
#   from langgraph.prebuilt import ToolNode, tools_condition
# YOUR CODE HERE


# STEP 1 — define AgentState, a TypedDict with one field, messages, annotated
# with LangGraph's add_messages reducer (Annotated[list, add_messages]) so
# each node's returned message APPENDS to the running list instead of
# replacing it.
# YOUR CODE HERE


# STEP 2 — write call_model(state: AgentState) -> dict:
#   - invoke model_with_tools.invoke(state["messages"])
#   - print whether the response has tool calls or is a final answer (same
#     intermediate-output debugging habit as exercise 01's inspect_tool_choice)
#   - return {"messages": [response]}
def call_model(state) -> dict:
    # YOUR CODE HERE
    pass


# STEP 3 — build a ToolNode from `tools` (the two-tool list from GIVEN):
#   tool_node = ToolNode(tools)
# YOUR CODE HERE


# STEP 4 — build the graph:
#   - builder = StateGraph(AgentState)
#   - add call_model and tool_node as nodes (name the tool node "tools")
#   - connect START to call_model
#   - add a conditional edge from call_model using tools_condition, mapping
#     its "tools" outcome to your tool node and its "__end__" outcome to END
#   - add the ONE NEW EDGE this exercise introduces: a plain edge from your
#     tool node BACK to call_model, closing the loop
#   - compile the graph into `agent`
# YOUR CODE HERE


# STEP 5 — invoke agent with TWO_TOOL_MESSAGE wrapped as a HumanMessage in
# the initial messages list, and print every message in the final state
# (its type and its content) so you can see the full back-and-forth: the
# model's first tool request, the tool's result, the model's second
# decision, and so on until a final answer with no more tool calls.
# YOUR CODE HERE


# EXPECTED BEHAVIOR ONCE IMPLEMENTED
# -----------------------------------
# Running TWO_TOOL_MESSAGE through the compiled agent should show call_model
# being invoked more than once (visible from Step 2's printed output): an
# initial decision (probably requesting one tool), a decision informed by
# that tool's result (requesting the second tool, or answering directly if
# the first result already covered everything), and a final answer with no
# further tool calls. Exercise 03 verifies this behavior more rigorously,
# contrasting a one-tool message against a two-tool message side by side.
#
# One thing this graph does NOT yet have: anything stopping it from looping
# forever if the model never stops requesting tool calls. That gap is
# exercise 04's job, not an oversight - an ungoverned loop should never run
# against a real task before a stopping condition exists.
#
# Common Pitfalls:
# - Forgetting the add_messages annotation on `messages`, which causes each
#   node's return value to REPLACE the message history instead of appending
#   to it, silently erasing what the loop needs to remember between passes.
# - Mapping tools_condition's outcomes incorrectly in add_conditional_edges
#   (swapping which string maps to the tool node versus END), which either
#   skips tool calls entirely or never recognizes a final answer.
# - Forgetting the loop-closing edge from the tool node back to call_model,
#   which leaves the graph compiling fine but behaving exactly like a
#   non-looping chain - one tool call, then nowhere further to go.
