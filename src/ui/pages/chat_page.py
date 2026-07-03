import streamlit as st

from src.ui.components.chat_message import render_history_message
from src.ui.components.kb_selector import render_kb_selector
from src.ui.components.tool_trace import format_tool_event
from src.ui.theme import render_page_hero


QUICK_PROMPTS = [
    "面试官问什么是 RAG，我怎么口语化回答并举一个生产案例？",
    "Embedding 在 RAG 里起什么作用？请用实际项目解释。",
    "如何降低大模型幻觉？请按面试表达方式组织回答。",
    "Agent 和普通 RAG 问答有什么区别？举客服场景例子。",
]


def render_chat_page(container) -> None:
    knowledge_bases = container.knowledge_base_service.list_knowledge_bases()
    render_page_hero(
        eyebrow="AI 问答工作台",
        title="智能客服对话",
        subtitle="把界面重做成接近参考图的中央工作区。左侧是启用中的知识域，右侧是欢迎区、快捷提问、流式回答、工具过程和知识来源。",
    )

    if not knowledge_bases:
        st.info("请先到“知识库管理”页面创建知识库并上传 Markdown 文档。")
        return

    with st.sidebar:
        st.subheader("对话配置")
        platform = st.selectbox(
            "模型平台",
            options=container.provider_service.list_platforms(),
            index=container.provider_service.list_platforms().index(
                st.session_state.get("chat_platform", container.settings.default_chat_platform)
            ),
        )
        default_model = container.provider_service.get_default_model(platform)
        model_name = st.text_input(
            "模型名称",
            value=st.session_state.get("chat_model_name") or default_model,
            help="可按需改成平台中实际可用的模型名",
        )
        st.session_state["chat_platform"] = platform
        st.session_state["chat_model_name"] = model_name
        prefilling_kb_ids = st.session_state.get("chat_prefill_kb_ids", [])
        if prefilling_kb_ids:
            st.session_state["selected_kb_ids"] = prefilling_kb_ids
        selected_kb_ids = render_kb_selector(knowledge_bases)

    enabled_kbs = [kb for kb in knowledge_bases if kb.id in selected_kb_ids]
    total_messages = len(st.session_state["chat_messages"])
    chat_col, main_col = st.columns([0.34, 0.66], gap="large")

    with chat_col:
        with st.container(border=True):
            st.markdown('<div class="panel-title">启用知识库</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="panel-subtitle">多知识库可同时参与检索。当前工作台会优先展示已启用的知识域。</div>',
                unsafe_allow_html=True,
            )
            if enabled_kbs:
                chips_html = "".join(
                    [
                        f'<div class="kb-chip active">● {kb.name}</div>'
                        for kb in enabled_kbs
                    ]
                )
                st.markdown(f'<div class="chip-row">{chips_html}</div>', unsafe_allow_html=True)
            else:
                st.warning("当前没有启用任何知识库。")

            st.markdown(
                f"""
                <div class="metric-strip" style="grid-template-columns:1fr;">
                    <div class="metric-chip">
                        <div class="metric-label">当前会话消息数</div>
                        <div class="metric-value">{total_messages}</div>
                    </div>
                    <div class="metric-chip">
                        <div class="metric-label">当前模型</div>
                        <div class="metric-value" style="font-size:1.05rem;">{model_name}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with st.container(border=True):
            st.markdown('<div class="panel-title">快捷提问</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="panel-subtitle">像参考图里的推荐问题一样，点一下就能把问题带到对话输入区。</div>',
                unsafe_allow_html=True,
            )
            for idx, prompt in enumerate(QUICK_PROMPTS, start=1):
                if st.button(prompt, key=f"quick_prompt_{idx}", use_container_width=True):
                    st.session_state["chat_prefill_text"] = prompt
                    st.rerun()

    with main_col:
        with st.container(border=True):
            title = "欢迎来到 AI 知识库问答台" if total_messages == 0 else "继续你的知识问答"
            subtitle = (
                "先选知识库，再提问。回答会展示工具调用过程和命中的知识来源。"
                if total_messages == 0
                else "当前会话已保留历史消息、知识来源和工具过程。"
            )
            st.markdown(
                f"""
                <div class="panel-title" style="font-size:2rem; margin-bottom:0.35rem;">{title}</div>
                <div class="panel-subtitle" style="font-size:1rem;">{subtitle}</div>
                """,
                unsafe_allow_html=True,
            )
            chips_html = "".join(
                [f'<div class="kb-chip active">{kb.name}</div>' for kb in enabled_kbs[:6]]
            )
            if chips_html:
                st.markdown(f'<div class="chip-row" style="margin-top:0.3rem;">{chips_html}</div>', unsafe_allow_html=True)
            if total_messages == 0:
                quick_html = "".join([f'<div class="quick-pill">{prompt}</div>' for prompt in QUICK_PROMPTS])
                st.markdown(f'<div class="quick-grid">{quick_html}</div>', unsafe_allow_html=True)

        for message in st.session_state["chat_messages"]:
            render_history_message(message)

        prefill_text = st.session_state.get("chat_prefill_text", "").strip()
        if prefill_text:
            st.info("已从快捷问题或知识库检索结果带入内容，你可以直接发送，或先修改后再发送。")
            with st.form("prefill_chat_form", clear_on_submit=False):
                user_query = st.text_area(
                    "待发送问题",
                    value=prefill_text,
                    height=220,
                )
                send_prefill = st.form_submit_button("发送到对话", use_container_width=True)
            if not send_prefill:
                return
            st.session_state["chat_prefill_text"] = ""
            st.session_state["chat_prefill_kb_ids"] = []
        else:
            user_query = st.chat_input("请输入用户问题")
            if not user_query:
                return

        if not selected_kb_ids:
            st.warning("当前没有启用任何知识库，请先在左侧勾选知识库后再提问。")
            return

        st.session_state["chat_messages"].append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        history = [
            {"role": item["role"], "content": item["content"]}
            for item in st.session_state["chat_messages"][:-1]
        ]
        answer_text = ""
        sources: list[dict] = []
        tool_lines: list[str] = []

        with st.chat_message("assistant"):
            answer_placeholder = st.empty()
            tool_placeholder = st.empty()
            source_placeholder = st.empty()

            try:
                for event in container.chat_service.stream_reply(
                    history=history,
                    user_query=user_query,
                    knowledge_base_ids=selected_kb_ids,
                    platform=platform,
                    model_name=model_name,
                ):
                    if event["type"] == "token":
                        answer_text = event["text"]
                        answer_placeholder.markdown(answer_text)
                    elif event["type"] == "sources":
                        sources = event["sources"]
                        with source_placeholder.container():
                            unique_targets = []
                            seen = set()
                            for source in sources:
                                key = (
                                    source["knowledge_base_name"],
                                    source["document_name"],
                                )
                                if key not in seen:
                                    seen.add(key)
                                    unique_targets.append(key)
                            if unique_targets:
                                target_text = "；".join(
                                    [f"{kb_name} / {doc_name}" for kb_name, doc_name in unique_targets]
                                )
                                st.info(f"本轮命中知识来源：{target_text}")
                            with st.expander("引用片段", expanded=False):
                                for source in sources:
                                    st.markdown(
                                        f"- **{source['knowledge_base_name']} / {source['document_name']}** "
                                        f"(score={source['score']})"
                                    )
                                    st.caption(source["preview"])
                    elif event["type"] == "tool":
                        line = format_tool_event(event["event"])
                        if line:
                            tool_lines.append(line)
                            with tool_placeholder.container():
                                with st.expander("工具调用过程", expanded=True):
                                    for item in tool_lines:
                                        st.write(item)
                    elif event["type"] == "done" and not answer_text:
                        answer_text = event["answer"]
                        answer_placeholder.markdown(answer_text)
            except Exception as exc:
                answer_text = f"对话执行失败: {exc}"
                answer_placeholder.error(answer_text)

        st.session_state["chat_messages"].append(
            {
                "role": "assistant",
                "content": answer_text,
                "sources": sources,
                "tool_events": tool_lines,
            }
        )
