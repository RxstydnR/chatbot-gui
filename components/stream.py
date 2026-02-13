
import streamlit as st
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import Command
from components.session import get_session_history, set_session_history

def process_stream(user_input: dict[str, list[dict[str, str]]] | Command) -> None:

    agent = st.session_state["agent"]
    
    events = agent.stream(
        user_input,
        config=st.session_state["config"],
        # stream_mode="values",
        debug=False
    )

    chat_history = get_session_history(st.session_state["session_id"])

    for event in events:
        for value in event.values():
            for message in value.get("messages", []):

                if isinstance(message, AIMessage):

                    if len(message.content) > 0:
                        st.chat_message("ai").write(message.content)
                        chat_history["main"].append(AIMessage(content=message.content))
                        chat_history["display"].append(AIMessage(content=message.content))

                    if message.tool_calls:
                        st.info(f"Tool call detected: {len(message.tool_calls)}")
                        for tool_call in message.tool_calls:
                            ui_request = {
                                "name": tool_call["name"],
                                "args": tool_call["args"],
                                "id": tool_call["id"]
                            }
                            ai_question_in_tool = tool_call["args"].get('question',None)
                            st.chat_message("ai").write(ai_question_in_tool)
                            # chat_history.append(ToolMessage(content=ai_question_in_tool, tool_call_id=tool_call["id"]))
                            # chat_history.append(AIMessage(content=ai_question_in_tool))
                            chat_history["main"].append(ToolMessage(content=ai_question_in_tool, tool_call_id=tool_call["id"]))
                            chat_history["display"].append(AIMessage(content=ai_question_in_tool, tool_call_id=tool_call["id"]))
                            set_session_history(st.session_state["session_id"], chat_history) # render後に後で移動
                            
                            return ui_request
                    else:
                        return None