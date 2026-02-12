import uuid
from typing import List
import streamlit as st

@st.dialog("チャット履歴をすべて削除してもよろしいですか？")
def delete_chat_history(session_id):
    if st.button("はい"):
        store = st.session_state["chat_history"]
        if len(store[session_id]) > 0:
            store[session_id] = []
            st.session_state["thread_id"] = uuid.uuid4().hex
            st.rerun()
        else:
            st.warning("チャット履歴がありません。")

def get_session_history(session_id: str) -> List:
    store = st.session_state["chat_history"]
    if session_id not in store:
        store[session_id] = []
    return store[session_id]

def set_session_history(session_id: str, chat_history: List) -> None:
    store = st.session_state["chat_history"]
    if session_id not in store:
        store[session_id] = []
    store[session_id] = chat_history