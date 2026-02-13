# from typing import Sequence
# from typing_extensions import Annotated, TypedDict
# from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agents.state import State
from agents.nodes import agent_node
from tools.ui_tools import UI_TOOLS

def create_graph():

    graph_builder = StateGraph(State)
    tool_node = ToolNode(tools=UI_TOOLS)
    graph_builder.add_node("agent", agent_node)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges("agent", tools_condition)
    graph_builder.add_edge("tools", "agent")
    graph_builder.set_entry_point("agent")
    graph = graph_builder.compile(
        checkpointer=MemorySaver(),
        interrupt_before=["tools"],
    )   
    return graph