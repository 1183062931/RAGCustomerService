from pathlib import Path

import streamlit as st

from src.bootstrap.container import ServiceContainer
from src.ui.navigation import build_navigation
from src.ui.state import initialize_session_state
from src.ui.theme import apply_theme, render_sidebar_brand


@st.cache_resource
def get_container() -> ServiceContainer:
    container = ServiceContainer(Path(__file__).parent)
    container.settings.ensure_directories()
    return container


def main() -> None:
    st.set_page_config(
        page_title="RAG 智能客服",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_theme()
    initialize_session_state()
    render_sidebar_brand()
    container = get_container()
    navigation = build_navigation(container)
    navigation.run()


if __name__ == "__main__":
    main()
