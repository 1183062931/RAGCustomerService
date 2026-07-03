import streamlit as st


def render_kb_selector(knowledge_bases: list) -> list[str]:
    options = {f"{kb.name} ({kb.id[:8]})": kb.id for kb in knowledge_bases}
    all_ids = list(options.values())
    selected_ids = [
        kb_id for kb_id in st.session_state.get("selected_kb_ids", []) if kb_id in all_ids
    ]
    if not selected_ids:
        selected_ids = all_ids

    default_labels = [label for label, kb_id in options.items() if kb_id in selected_ids]
    selected_labels = st.multiselect(
        "启用知识库",
        options=list(options.keys()),
        default=default_labels,
        key="selected_kb_labels",
        help="可同时勾选多个知识库进行检索",
    )
    selected_ids = [options[label] for label in selected_labels]
    st.session_state["selected_kb_ids"] = selected_ids
    return selected_ids
