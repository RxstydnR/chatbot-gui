import uuid
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,ToolMessage,SystemMessage, AIMessage
from langgraph.types import Command

from agents.graph import create_graph
from agents.prompt import SYSTEM_PROMPT_TEMPLATE
from components.renderer import render_gui_parts
from components.session import get_session_history, set_session_history, delete_chat_history
from components.init_page import render_init_page, SUGGESTIONS
from components.stream import process_stream

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
if "user_first_interaction" not in st.session_state:
    st.session_state["user_first_interaction"] = False


with st.sidebar:

    st.space("small")
    
    st.button(
        "Delete Chat History\n",
        on_click=delete_chat_history, 
        args=(st.session_state["session_id"],),
        width="stretch",
        type="primary"
    )
    st.button(
        "Clear All Sessions", 
        on_click=lambda: st.session_state.clear(),
        width="stretch",
        type="secondary"
    )


# 初期画面用の表示判定
user_just_asked_initial_question = (
    "initial_question" in st.session_state and st.session_state.initial_question
)
user_just_clicked_suggestion = (
    "selected_suggestion" in st.session_state and st.session_state.selected_suggestion
)
if user_just_asked_initial_question or user_just_clicked_suggestion:
    st.session_state["user_first_interaction"] = True

# Show a different UI when the user hasn't asked a question yet.
if not st.session_state["user_first_interaction"]:
    render_init_page()
    st.stop()
else:
    st.session_state["user_first_interaction"] = True

# ユーザの入力受付
prompt = st.chat_input("メッセージを入力...")
if not prompt:

    if user_just_asked_initial_question:
        prompt = st.session_state.initial_question
    
    if user_just_clicked_suggestion:
        prompt = SUGGESTIONS[st.session_state.selected_suggestion]

# システムプロンプトの追加
chat_history = get_session_history(st.session_state["session_id"])
if len(chat_history["main"]) == 0:
    chat_history["main"].append(SystemMessage(content=SYSTEM_PROMPT_TEMPLATE))
    chat_history["display"].append(SystemMessage(content=SYSTEM_PROMPT_TEMPLATE))
    set_session_history(st.session_state["session_id"], chat_history)

# 履歴表示
chat_history = get_session_history(st.session_state["session_id"])
if len(chat_history["display"]) > 0:
    for message in chat_history["display"]:
        if isinstance(message, (HumanMessage, ToolMessage)):
            role = "user" 
        elif isinstance(message, SystemMessage):
            continue
        else:
            role = "ai"

        if message.content:
            with st.chat_message(role):
                st.write(message.content)

        if hasattr(message, "tool_calls"):
            for tool_call in message.tool_calls:
                ai_question_in_tool = tool_call["args"].get('question',None)
                if ai_question_in_tool:
                    st.chat_message("ai").write(ai_question_in_tool)


# Agentの呼び出し
if prompt or (not st.session_state.user_turn):
    
    if prompt:

        # ユーザの入力を表示する
        st.chat_message("user").write(prompt)
        # 会話履歴の追加
        chat_history["main"].append(HumanMessage(content=prompt))
        chat_history["display"].append(HumanMessage(content=prompt))
        set_session_history(st.session_state["session_id"], chat_history)
    
    # Userの返答はToolMessageとして既にchat_historyに追加されている
    ui_request = process_stream({"messages":[chat_history["main"][-1]]})

    if ui_request:
        st.session_state.user_turn = True
        render_gui_parts(ui_request)
    else:
        st.session_state.user_turn = False
        # 会話履歴の追加
        chat_history["main"].append(HumanMessage(content="ツールを利用してください。"))
        set_session_history(st.session_state["session_id"], chat_history)