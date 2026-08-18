from langchain_core.tools import BaseTool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage, AIMessage
from src.states.chat_state import ChatState
from src.database.checkpointers.checkpointer_factory import CheckpointerFactory
from src.chat_models.chat_model import ChatModel
from src.mcp.mcp_tool_utility import load_tools
from src.utility.chat_cleanup import cleanup_chat
from src.utility.system_message import load_mipa_system_message
from typing import Literal


# CHAT CLEANUP NODE IMPLEMENTATION
def chat_cleanup_node(state: ChatState, config: RunnableConfig) -> dict:
    chat_model: ChatModel = config["configurable"]["chat_model"]
    messages: list[BaseMessage] = state.messages
    summary: str = state.summary

    return cleanup_chat(chat_model, messages, summary)


# CHAT NODE IMPLEMENTATION
def chat_node(state: ChatState, config: RunnableConfig) -> dict:
    chat_model: ChatModel = config["configurable"]["chat_model"]
    username: str = config["configurable"]["username"]
    messages: list[BaseMessage] = state.messages
    summary: str = state.summary

    system_message = load_mipa_system_message(username, summary)

    response = chat_model.invoke([system_message] + messages)

    return {
        "messages": [response],
        "summary": summary
    }


def router(state: ChatState, config: RunnableConfig) -> Literal["YES", "NO"]:
    messages = state.messages
    last_message = messages[-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "YES"

    return "NO"


# MUST PASS THE CHECKPOINTER IMPLEMENTATION YOU WANT
async def load_chatbot(checkpointer_factory: CheckpointerFactory) -> CompiledStateGraph:
    # LOAD TOOLS
    tools: list[BaseTool] = await load_tools()
    if len(tools) == 0:
        print("COULD NOT CONNECT TO THE MCP SERVER(S)")

    # GET THE TOOL NODE ANYWAY
    tool_node = ToolNode(
        tools=tools
    )

    # LOAD THE PERSISTENCE CHECKPOINTER
    checkpointer = checkpointer_factory.load_checkpointer()

    # GET THE GRAPH
    graph = StateGraph(state_schema=ChatState)

    # ADD NODES
    graph.add_node("chat_node", chat_node)
    graph.add_node("tool_node", tool_node)
    graph.add_node("chat_cleanup_node", chat_cleanup_node)

    # ADD EDGES
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges(
        "chat_node",
        router,
        {
            "YES": "tool_node",
            "NO": "chat_cleanup_node"
        }
    )
    graph.add_edge("tool_node", "chat_node")
    graph.add_edge("chat_cleanup_node", END)

    chatbot = graph.compile(
        checkpointer=checkpointer
    )

    return chatbot
