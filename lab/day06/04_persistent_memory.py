"""
EXERCISE 04 — Persistent multi-turn context with a checkpointer

CONCEPT
-------
Exercises 02-03's chain is stateless between separate invocations: call it
once, get a reply, call it again, and it has no idea a previous call ever
happened. That's fine for one self-contained message. It's not fine for a
guest sending a FOLLOW-UP message that only makes sense in light of what
they already said ("it's also leaking now" means nothing without the first
message about the AC).

The current recommended way to persist state across separate calls is a
CHECKPOINTER, compiled into the graph, keyed by a thread_id: every call
against the same thread_id reads the previous checkpoint back into state
before its nodes run, and a DIFFERENT thread_id gets a fully separate
history. The conversation history itself lives in a state field annotated
with `add_messages`, which appends new messages to the list instead of
overwriting it - the field-overwrite behavior every other state field in
this exercise set uses.

(Older LangChain versions used dedicated memory classes like
ConversationBufferMemory, attached directly to a chain. Those moved to a
separate langchain-classic package for old code only - this exercise uses
the current, non-legacy approach.)

RUNNING SCENARIO
-----------------
The same guest sends a first message, then a follow-up that depends on it.
# [Placeholder — replace with your team's actual Sprint 3 AI feature]

SETUP
-----
    pip install langchain langgraph langchain-anthropic langchain-openai python-dotenv
    export ANTHROPIC_API_KEY=...      # and/or
    export OPENAI_API_KEY=...
"""

# =============================================================================
# GIVEN — the sample data for this exercise. Nothing to change here.
# =============================================================================

FIRST_MESSAGE = "The AC in room 214 won't turn off."
FOLLOWUP_MESSAGE = "It's also leaking water now."

RESPONSE_TEMPLATE_TEXT = (
    "You are a helpful hotel guest-services assistant. "
    "Draft a short, courteous reply to the guest. "
    "Use the conversation history to understand follow-up messages and "
    "acknowledge relevant earlier details."
)

# Two different guests, to prove thread-scoping actually isolates them.
THREAD_ID_GUEST_A = "guest-214"
THREAD_ID_GUEST_B = "guest-999"

MODEL = "openai:gpt-5.4-mini"  # or "openai:gpt-5.6"


# =============================================================================
# YOUR TURN — write the code for each step below the comment that describes
# it.
# =============================================================================

# STEP 0 — imports and model.
#   from typing import Annotated
#   from typing_extensions import TypedDict
#   from langgraph.graph import StateGraph, START, END
#   from langgraph.graph.message import add_messages
#   from langgraph.checkpoint.memory import InMemorySaver
#   from langchain_core.messages import HumanMessage
#   from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
#   from langchain.chat_models import init_chat_model
#   model = init_chat_model(MODEL)



# STEP 1 — define the state: a TypedDict named ConversationState with ONE
# field, messages, typed as Annotated[list, add_messages]. This annotation
# is what makes new messages APPEND to the list on each call instead of
# replacing it - the mechanism the whole exercise depends on.



# STEP 2 — write respond_node(state: ConversationState) -> dict:
#   - format response_template with state["messages"]. The messages
#     placeholder preserves the entire structured conversation history,
#     while the system prompt gives the reply consistent instructions.
#   - call model.invoke(...) with the formatted prompt
#   - the result is already a proper AIMessage - return
#     {"messages": [result]} (a list containing just the NEW message; the
#     add_messages annotation appends it to what's already there, it does
#     not replace the whole list)


# STEP 3 — build the graph WITH a checkpointer:
#   builder = StateGraph(ConversationState)
#   builder.add_node("respond_node", respond_node)
#   builder.add_edge(START, "respond_node")
#   builder.add_edge("respond_node", END)
#   chain = builder.compile(checkpointer=PersistentSaver("checkpoint_file"))



# STEP 4 — invoke the chain TWICE with the SAME thread_id
# (THREAD_ID_GUEST_A), passing a config dict each time:
#   config = {"configurable": {"thread_id": THREAD_ID_GUEST_A}}
#   call 1: chain.invoke({"messages": [HumanMessage(content=FIRST_MESSAGE)]}, config)
#   call 2: chain.invoke({"messages": [HumanMessage(content=FOLLOWUP_MESSAGE)]}, config)
# After each call, print len(result["messages"]) and each message's
# content - the count should grow by 2 each call (one human, one AI), and
# call 2's reply should read as if it knows about the AC issue from call 1.



# STEP 5 — invoke the chain ONCE MORE with a DIFFERENT thread_id
# (THREAD_ID_GUEST_B) and FOLLOWUP_MESSAGE alone. Print the message count
# and contents again - it should start fresh, with no trace of guest A's
# conversation, proving thread-scoping isolates separate guests.
# config_guest_b = {"configurable": {"thread_id": THREAD_ID_GUEST_B}}
# result_3 = chain.invoke(
#     {"messages": [HumanMessage(content=FOLLOWUP_MESSAGE)]},
#     config_guest_b,
# )
# print(len(result_3["messages"]))
# for msg in result_3["messages"]:
#     print(msg.content)

# What this demonstrates:
# A checkpointer plus a thread_id gives a chain short-term, thread-scoped
# memory with no change to the nodes themselves - the same respond_node
# works whether or not a checkpointer is attached. The isolation check in
# Step 5 is the part that matters most in production: memory that leaked
# across guests would be a real bug, not just a missing feature.
