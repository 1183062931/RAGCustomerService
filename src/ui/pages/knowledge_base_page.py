import streamlit as st

from src.ui.components.highlight import highlight_text
from src.ui.theme import render_page_hero


def render_knowledge_base_page(container) -> None:
    service = container.knowledge_base_service
    search_service = container.search_service
    knowledge_bases = service.list_knowledge_bases()
    total_documents = sum(len(service.list_documents(kb.id)) for kb in knowledge_bases)
    ready_documents = sum(
        1
        for kb in knowledge_bases
        for doc in service.list_documents(kb.id)
        if doc.status == "ready"
    )

    render_page_hero(
        eyebrow="知识资产台",
        title="知识库管理",
        subtitle="按参考图的方向重做为玻璃感工作台。你可以在这里创建知识库、上传 Markdown 文档、做相近内容检索，并把命中的片段一键带去对话页继续追问。",
    )

    st.markdown(
        f"""
        <div class="metric-strip">
            <div class="metric-chip">
                <div class="metric-label">知识库数量</div>
                <div class="metric-value">{len(knowledge_bases)}</div>
            </div>
            <div class="metric-chip">
                <div class="metric-label">文档总数</div>
                <div class="metric-value">{total_documents}</div>
            </div>
            <div class="metric-chip">
                <div class="metric-label">可检索文档</div>
                <div class="metric-value">{ready_documents}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    overview_col, action_col = st.columns([1.1, 1.35], gap="large")

    with overview_col:
        with st.container(border=True):
            st.markdown('<div class="panel-title">知识库总览</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="panel-subtitle">用卡片快速查看每个知识库的规模、创建时间和说明。</div>',
                unsafe_allow_html=True,
            )
            if not knowledge_bases:
                st.info("暂无知识库，先在右侧创建一个新的知识库。")
            else:
                for kb in knowledge_bases:
                    documents = service.list_documents(kb.id)
                    ready_count = len([doc for doc in documents if doc.status == "ready"])
                    st.markdown(
                        f"""
                        <div class="result-card" style="margin-bottom:0.85rem;">
                            <div class="result-title">{kb.name}</div>
                            <div class="result-meta">创建时间：{kb.created_at[:19].replace('T', ' ')} · 文档 {len(documents)} 份 · 可检索 {ready_count} 份</div>
                            <div style="color:#5f698d; line-height:1.75;">{kb.description or "暂无说明"}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    with action_col:
        create_col, upload_col = st.columns([0.95, 1.05], gap="medium")

        with create_col:
            with st.container(border=True):
                st.markdown('<div class="panel-title">新建知识库</div>', unsafe_allow_html=True)
                st.markdown(
                    '<div class="panel-subtitle">建议按业务域拆分，后续对话时可多选组合检索。</div>',
                    unsafe_allow_html=True,
                )
                with st.form("create_kb_form", clear_on_submit=True):
                    name = st.text_input("知识库名称", placeholder="例如：售后FAQ知识库")
                    description = st.text_area(
                        "知识库说明",
                        height=150,
                        placeholder="简要说明内容范围、适用部门、使用场景",
                    )
                    submitted = st.form_submit_button("创建知识库", use_container_width=True)
                    if submitted:
                        if not name.strip():
                            st.warning("知识库名称不能为空")
                        else:
                            try:
                                service.create_knowledge_base(name=name, description=description)
                            except Exception as exc:
                                st.error(f"创建失败: {exc}")
                            else:
                                st.success("知识库已创建")
                                st.rerun()

        with upload_col:
            with st.container(border=True):
                st.markdown('<div class="panel-title">上传与入库</div>', unsafe_allow_html=True)
                st.markdown(
                    '<div class="panel-subtitle">选择目标知识库后上传 Markdown 文件，系统会自动切分并向量化。</div>',
                    unsafe_allow_html=True,
                )
                if not knowledge_bases:
                    st.info("请先创建知识库")
                else:
                    kb_options = {f"{kb.name} ({kb.id[:8]})": kb.id for kb in knowledge_bases}
                    selected_label = st.selectbox("目标知识库", list(kb_options.keys()))
                    selected_kb_id = kb_options[selected_label]
                    uploaded_files = st.file_uploader(
                        "选择 Markdown 文件",
                        type=["md", "markdown"],
                        accept_multiple_files=True,
                    )
                    if st.button("开始入库", use_container_width=True):
                        if not uploaded_files:
                            st.warning("请先选择文件")
                        else:
                            success_count = 0
                            for uploaded_file in uploaded_files:
                                with st.spinner(f"正在处理 {uploaded_file.name}"):
                                    try:
                                        service.ingest_uploaded_markdown(
                                            knowledge_base_id=selected_kb_id,
                                            filename=uploaded_file.name,
                                            content=uploaded_file.getvalue(),
                                        )
                                    except Exception as exc:
                                        st.error(f"{uploaded_file.name} 入库失败: {exc}")
                                    else:
                                        success_count += 1
                            st.success(f"已完成 {success_count} 个文件入库")
                            st.rerun()

                    documents = service.list_documents(selected_kb_id)
                    st.markdown("##### 当前文档")
                    if not documents:
                        st.info("当前知识库还没有文档")
                    else:
                        for document in documents[:8]:
                            st.markdown(
                                f"""
                                <div class="result-card" style="margin-bottom:0.7rem;">
                                    <div class="result-title">{document.filename}</div>
                                    <div class="result-meta">状态：{document.status} · 分块数：{document.chunk_count}</div>
                                    <div style="color:#6b728f;">{document.error_message or "已完成入库，可参与检索。"}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

    with st.container(border=True):
        st.markdown('<div class="panel-title">知识库检索测试</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="panel-subtitle">像参考图里的中央搜索工作区一样，直接输入问题查看相近内容、相似度和来源章节。</div>',
            unsafe_allow_html=True,
        )

        if not knowledge_bases:
            st.info("请先创建知识库并上传文档，才能体验检索测试。")
            return

        kb_options = {f"{kb.name} ({kb.id[:8]})": kb.id for kb in knowledge_bases}
        default_label = list(kb_options.keys())[0]
        search_controls, search_side = st.columns([1.25, 0.75], gap="large")

        with search_controls:
            search_kb_labels = st.multiselect(
                "选择要检索的知识库",
                options=list(kb_options.keys()),
                default=[default_label],
                key="kb_search_labels",
                help="可同时选择多个知识库，查看最相近的内容片段",
            )
            search_query = st.text_area(
                "输入搜索问题",
                placeholder="例如：什么是 RAG，为什么企业项目不用纯大模型直答？",
                height=130,
            )

        with search_side:
            doc_name_filter = st.text_input(
                "按文档名过滤",
                placeholder="例如：ai_interview_questions",
                help="先完成检索，再按文档名筛选结果",
            )
            search_limit = st.slider("返回片段数", min_value=1, max_value=10, value=5)
            do_search = st.button("搜索相近内容", use_container_width=True)

        if do_search:
            selected_ids = [kb_options[label] for label in search_kb_labels]
            if not selected_ids:
                st.warning("请至少选择一个知识库")
            elif not search_query.strip():
                st.warning("请输入搜索问题")
            else:
                results = search_service.search_similar_content(
                    query=search_query,
                    knowledge_base_ids=selected_ids,
                    limit=search_limit,
                )
                lowered_filter = doc_name_filter.strip().lower()
                if lowered_filter:
                    results = [
                        result
                        for result in results
                        if lowered_filter in result.document_name.lower()
                    ]

                if not results:
                    st.info("没有检索到相近内容")
                else:
                    st.success(f"已找到 {len(results)} 个相近片段")
                    for index, result in enumerate(results, start=1):
                        section_title = result.metadata.get("section_title")
                        st.markdown(
                            f"""
                            <div class="result-card" style="margin-bottom:0.9rem;">
                                <div class="result-title">#{index} {result.knowledge_base_name} / {result.document_name}</div>
                                <div class="result-meta">相似度分数：{result.score:.4f} · 文档ID：{result.document_id} · 章节：{section_title or "未标注"}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"""
                            <div class="search-result-body">
                                {highlight_text(result.content, search_query)}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            "带入对话页",
                            key=f"send_to_chat_{result.chunk_id}",
                            use_container_width=True,
                        ):
                            from src.ui.navigation import get_chat_page

                            st.session_state["chat_prefill_text"] = (
                                f"请基于这段知识片段继续解释，并整理成适合面试现场的口语化回答：\n\n"
                                f"知识库：{result.knowledge_base_name}\n"
                                f"文档：{result.document_name}\n"
                                f"章节：{section_title or '未标注'}\n\n"
                                f"{result.content}"
                            )
                            st.session_state["chat_prefill_kb_ids"] = [result.knowledge_base_id]
                            st.switch_page(get_chat_page())
