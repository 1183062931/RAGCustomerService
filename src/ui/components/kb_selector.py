import streamlit as st


def render_kb_selector(knowledge_bases: list) -> list[str]:
    all_ids = [kb.id for kb in knowledge_bases]
    selected_ids = [
        kb_id for kb_id in st.session_state.get("selected_kb_ids", []) if kb_id in all_ids
    ]
    if not selected_ids:
        selected_ids = all_ids

    st.caption("可同时勾选多个知识库进行检索")
    next_selected_ids: list[str] = []
    for kb in knowledge_bases:
        checked = st.checkbox(
            kb.name,
            value=kb.id in selected_ids,
            key=f"kb_enabled_{kb.id}",
            help=kb.description or "该知识库暂无说明",
        )
        if checked:
            next_selected_ids.append(kb.id)

    selected_ids = next_selected_ids
    st.session_state["selected_kb_ids"] = selected_ids
    return selected_ids
