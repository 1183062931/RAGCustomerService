import streamlit as st

from src.ui.pages.chat_page import render_chat_page
from src.ui.pages.knowledge_base_page import render_knowledge_base_page

_container = None
_knowledge_base_page = None
_chat_page = None


def knowledge_base_view():
    render_knowledge_base_page(_container)


def chat_view():
    render_chat_page(_container)


def get_chat_page():
    return _chat_page


def build_navigation(container):
    global _container, _knowledge_base_page, _chat_page
    _container = container
    _knowledge_base_page = st.Page(
        knowledge_base_view,
        title="知识库管理",
        icon="📚",
        url_path="knowledge-base",
        default=True,
    )
    _chat_page = st.Page(
        chat_view,
        title="智能客服对话",
        icon="💬",
        url_path="chat",
    )
    return st.navigation([_knowledge_base_page, _chat_page])
