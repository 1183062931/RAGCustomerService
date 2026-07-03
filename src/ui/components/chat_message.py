import streamlit as st


def render_history_message(message: dict) -> None:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        sources = message.get("sources") or []
        if sources:
            with st.expander("引用片段", expanded=False):
                for source in sources:
                    st.markdown(
                        f"- **{source['knowledge_base_name']} / {source['document_name']}** "
                        f"(score={source['score']})"
                    )
                    st.caption(source["preview"])
        tool_events = message.get("tool_events") or []
        if tool_events:
            with st.expander("工具调用过程", expanded=False):
                for line in tool_events:
                    st.write(line)
