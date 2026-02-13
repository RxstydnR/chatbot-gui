from langchain_openai import ChatOpenAI

from src.agents.state import State
from src.agents.ui_tools import UI_TOOLS

def agent_node(state: State):

    llm = ChatOpenAI(
        model="gpt-5.2"
    ).bind_tools(
        UI_TOOLS, 
        tool_choice="required", 
        parallel_tool_calls=True
    )
    
    response = llm.invoke(state["messages"])
        
    return {
        "messages": [response]
    }