import streamlit as st
from src.styles.fadein import CHAR_FADEIN_ANIMATION_CSS
from src.styles.background import MAIN_APP_CONTENTS_CSS, CHAT_MESSAGE_CSS, SIDEBAR_CSS

def load_css():    
    st.markdown("""
    <style>
        .stAppViewBlockContainer {
            max-width: 80%;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(MAIN_APP_CONTENTS_CSS, unsafe_allow_html=True)
    st.markdown(CHAT_MESSAGE_CSS, unsafe_allow_html=True)
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    st.markdown(CHAR_FADEIN_ANIMATION_CSS, unsafe_allow_html=True)