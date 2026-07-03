import streamlit as st


def initialize_session_state() -> None:
    st.session_state.setdefault("chat_messages", [])
    st.session_state.setdefault("chat_platform", "openai")
    st.session_state.setdefault("chat_model_name", "")
    st.session_state.setdefault("selected_kb_ids", [])
    st.session_state.setdefault("chat_prefill_text", "")
    st.session_state.setdefault("chat_prefill_kb_ids", [])
