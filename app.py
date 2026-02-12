# Tool callでHuman in the loopした場合は聴いた場合は、Tool callで返さないといけない
# それがstreamlitと相性が悪いんだよなぁ...。

import uuid
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage,SystemMessage, AIMessage
from langgraph.types import Command

from agents.graph import create_graph
from agents.prompt import SYSTEM_PROMPT_TEMPLATE
from components.renderer import render_gui_parts
from components.session import get_session_history, set_session_history, delete_chat_history

# .envファイルから環境変数を読み込む
load_dotenv()

st.set_page_config(page_title="GUI Agent", layout="centered")

# CSS
from styles.style_loader import load_css
load_css()

# セッション初期化
if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid.uuid4().hex
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = uuid.uuid4().hex
if "messages" not in st.session_state:
    st.session_state.messages = []
if "ui_request" not in st.session_state:
    st.session_state.ui_request = None
if "user_turn" not in st.session_state:
    st.session_state.user_turn = True
if "agent" not in st.session_state:
    st.session_state["agent"] = create_graph()
if "config" not in st.session_state:
    st.session_state.config = {
        "configurable": {
            "thread_id": st.session_state["thread_id"]
        }
    }

with st.sidebar:
    st.button("Delete Chat History", on_click=delete_chat_history, args=(st.session_state["session_id"],))


# messageが0個ならsystempromptを先頭に追加
chat_history = get_session_history(st.session_state["session_id"])
if len(chat_history) == 0:
    chat_history.append(SystemMessage(content=SYSTEM_PROMPT_TEMPLATE))
    set_session_history(st.session_state["session_id"], chat_history)

# 履歴表示
chat_history = get_session_history(st.session_state["session_id"])
if len(chat_history) > 0:
    for message in chat_history:
        if isinstance(message, (HumanMessage, ToolMessage)):
            role = "user" 
        elif isinstance(message, SystemMessage):
            continue
        else:
            role = "assistant"

        if message.content:
            with st.chat_message(role):
                st.write(message.content)

with st.sidebar:
    for i, msg in enumerate(chat_history[1:]):
        st.write(msg)
        # st.write(msg.type)
        # st.write(msg.content)
        st.divider()

def process_stream(user_input: dict[str, list[dict[str, str]]] | Command) -> None:
# def process_stream(user_input: str) -> None:

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
                        chat_history.append(AIMessage(content=message.content))

                    if message.tool_calls:
                        st.info(len(message.tool_calls))
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
                            # chat_history.append(ToolMessage(content="", tool_call_id=tool_call["id"]))
                            set_session_history(st.session_state["session_id"], chat_history) # render後に後で移動
                            
                            return ui_request
                    else:
                        return None
                            

if (prompt := st.chat_input("メッセージを入力...")) or (not st.session_state.user_turn):
    
    if prompt:
        st.info("prompt received")

        # ユーザの入力を表示する
        st.chat_message("user").write(prompt)
        # 会話履歴の追加
        chat_history.append(HumanMessage(content=prompt))
        set_session_history(st.session_state["session_id"], chat_history)
        ui_request = process_stream({"messages":[chat_history[-1]]})
    else:
        # st.info("waiting for user input via tool...")
        ui_request = process_stream({"messages":[]})

    if ui_request:
        st.session_state.user_turn = True
        render_gui_parts(ui_request)
    else:
        st.session_state.user_turn = False
        # 会話履歴の追加
        chat_history.append(HumanMessage(content="ツールを利用してください。"))
        set_session_history(st.session_state["session_id"], chat_history)