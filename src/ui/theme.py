import streamlit as st


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700;800&display=swap');

        :root {
            --app-bg: #f4f6fb;
            --panel-bg: rgba(255, 255, 255, 0.9);
            --panel-strong: rgba(255, 255, 255, 0.97);
            --line-soft: rgba(95, 111, 214, 0.14);
            --text-main: #17233f;
            --text-soft: #4f5d7a;
            --brand-a: #30c7d2;
            --brand-b: #3f7cff;
            --brand-c: #d94ca8;
            --shadow-lg: 0 16px 44px rgba(91, 104, 181, 0.12);
            --shadow-md: 0 8px 22px rgba(91, 104, 181, 0.1);
            --radius-xl: 28px;
            --radius-lg: 22px;
            --radius-md: 16px;
        }

        html, body, [class*="css"]  {
            font-family: "Plus Jakarta Sans", "Noto Sans SC", sans-serif;
            color: var(--text-main);
        }

        .stApp {
            background:
                radial-gradient(circle at 18% 18%, rgba(74, 222, 255, 0.1), transparent 24%),
                radial-gradient(circle at 62% 12%, rgba(173, 132, 255, 0.1), transparent 20%),
                radial-gradient(circle at 28% 72%, rgba(255, 114, 182, 0.08), transparent 16%),
                linear-gradient(180deg, #f7f8fc 0%, #f2f4f9 100%);
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 10px;
            border-radius: 32px;
            border: 1px solid rgba(148, 163, 255, 0.12);
            pointer-events: none;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.3);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(245,247,252,0.98));
            border-right: 1px solid rgba(120, 135, 255, 0.08);
            backdrop-filter: blur(10px);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        [data-testid="stSidebarNav"] {
            background: transparent;
            padding-top: 0.75rem;
        }

        [data-testid="stSidebarNav"] ul {
            gap: 0.3rem;
        }

        [data-testid="stSidebarNav"] a {
            border-radius: 14px;
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(122, 133, 255, 0.04);
            margin-bottom: 0.22rem;
            box-shadow: none;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(255,255,255,1);
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: linear-gradient(90deg, rgba(130, 93, 255, 0.07), rgba(47, 193, 224, 0.06));
            border: 1px solid rgba(115, 102, 255, 0.16);
        }

        [data-testid="stSidebarNav"] a span {
            color: #24304f !important;
            font-weight: 600;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 1.6rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            letter-spacing: -0.03em;
        }

        .app-shell {
            padding: 0.25rem 0 0.75rem 0;
        }

        .page-hero {
            position: relative;
            overflow: hidden;
            padding: 1.9rem 2rem;
            border-radius: 30px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.98), rgba(249,250,255,0.95)),
                linear-gradient(135deg, rgba(48,199,210,0.08), rgba(217,76,168,0.08));
            border: 1px solid rgba(229,233,246,0.95);
            box-shadow: var(--shadow-lg);
        }

        .page-hero::before {
            content: "";
            position: absolute;
            inset: 0;
            padding: 1px;
            border-radius: 30px;
            background: linear-gradient(135deg, rgba(48,199,210,0.95), rgba(74,126,255,0.9), rgba(217,76,168,0.95));
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
        }

        .page-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.42rem 0.75rem;
            border-radius: 999px;
            background: rgba(247, 248, 255, 0.96);
            color: #5c4af2;
            font-size: 0.88rem;
            font-weight: 700;
            box-shadow: 0 6px 16px rgba(120, 99, 255, 0.08);
        }

        .page-title {
            margin: 1rem 0 0.35rem 0;
            font-size: clamp(2rem, 4vw, 3.2rem);
            font-weight: 800;
            line-height: 1.08;
            color: #1e2a4f;
        }

        .page-subtitle {
            max-width: 780px;
            color: var(--text-soft);
            font-size: 1rem;
            line-height: 1.8;
            margin: 0;
            font-weight: 500;
        }

        .glass-card {
            background: var(--panel-bg);
            border: 1px solid rgba(229,233,246,0.95);
            backdrop-filter: blur(12px);
            border-radius: 26px;
            box-shadow: var(--shadow-md);
            padding: 1.2rem 1.25rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--panel-bg);
            border: 1px solid rgba(229,233,246,0.95);
            backdrop-filter: blur(12px);
            border-radius: 26px;
            box-shadow: var(--shadow-md);
            padding: 0.3rem;
        }

        .panel-title {
            font-size: 1.1rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
            color: #1f294a;
        }

        .panel-subtitle {
            color: var(--text-soft);
            font-size: 0.95rem;
            margin-bottom: 1rem;
            line-height: 1.75;
            font-weight: 500;
        }

        .metric-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.9rem;
            margin-top: 1rem;
        }

        .metric-chip {
            padding: 1rem 1.05rem;
            border-radius: 22px;
            background: rgba(255,255,255,0.96);
            border: 1px solid rgba(226,231,245,0.95);
            box-shadow: 0 8px 18px rgba(120, 132, 255, 0.06);
        }

        .metric-label {
            color: #56637e;
            font-size: 0.84rem;
            margin-bottom: 0.25rem;
            font-weight: 600;
        }

        .metric-value {
            font-size: 1.45rem;
            font-weight: 800;
            color: #1c2748;
        }

        .chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }

        .kb-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.48rem 0.82rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.96);
            border: 1px solid rgba(221,226,244,0.95);
            color: #223156;
            font-size: 0.9rem;
            box-shadow: 0 6px 16px rgba(115, 121, 255, 0.05);
            font-weight: 600;
        }

        .kb-chip.active {
            background: linear-gradient(135deg, rgba(116, 96, 255, 0.08), rgba(53, 196, 229, 0.08));
            border-color: rgba(114, 101, 255, 0.16);
        }

        .result-card {
            position: relative;
            overflow: hidden;
            padding: 1.15rem 1.15rem 0.95rem;
            border-radius: 24px;
            background: linear-gradient(180deg, rgba(255,255,255,1), rgba(249,250,255,0.98));
            border: 1px solid rgba(226,231,245,0.95);
            box-shadow: 0 10px 24px rgba(112, 126, 255, 0.08);
        }

        .result-card::before {
            content: "";
            position: absolute;
            inset: auto 0 0 0;
            height: 4px;
            background: linear-gradient(90deg, var(--brand-a), var(--brand-b), var(--brand-c));
            opacity: 0.92;
        }

        .result-title {
            font-weight: 800;
            font-size: 1.02rem;
            color: #1f294c;
            margin-bottom: 0.3rem;
        }

        .result-meta {
            color: #596884;
            font-size: 0.87rem;
            margin-bottom: 0.85rem;
            font-weight: 500;
        }

        .search-result-body {
            margin: -0.25rem 0 0.95rem;
            padding: 1rem 1.05rem;
            border-radius: 18px;
            background: #ffffff;
            border: 1px solid rgba(226, 231, 245, 0.95);
            color: #1f2a44 !important;
            line-height: 1.85;
            font-size: 0.96rem;
            font-weight: 500;
            box-shadow: 0 8px 18px rgba(113, 127, 255, 0.05);
        }

        .search-result-body,
        .search-result-body p,
        .search-result-body div,
        .search-result-body span,
        .search-result-body li,
        .search-result-body strong,
        .search-result-body em {
            color: #1f2a44 !important;
        }

        .chat-shell {
            display: grid;
            grid-template-columns: 340px minmax(0, 1fr);
            gap: 1.2rem;
            align-items: start;
        }

        .chat-composer-card {
            padding: 1.1rem;
            border-radius: 28px;
            background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(248,249,255,0.96));
            border: 1px solid rgba(229,233,246,0.95);
            box-shadow: var(--shadow-lg);
        }

        .quick-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.8rem;
            margin-top: 1rem;
        }

        .quick-pill {
            padding: 0.85rem 1rem;
            border-radius: 18px;
            background: rgba(255,255,255,0.96);
            border: 1px dashed rgba(128, 140, 255, 0.12);
            color: #2b365d;
            font-size: 0.92rem;
            font-weight: 600;
        }

        .sidebar-brand {
            padding: 0.25rem 0.2rem 0.8rem 0.2rem;
        }

        .sidebar-brand-title {
            font-size: 1.72rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: #172347;
        }

        .sidebar-brand-title span {
            background: linear-gradient(135deg, var(--brand-a), var(--brand-b), var(--brand-c));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .sidebar-brand-subtitle {
            color: #55637f;
            font-size: 0.86rem;
            line-height: 1.65;
            margin-top: 0.35rem;
            font-weight: 500;
        }

        .sidebar-floating-note {
            display: none;
        }

        div[data-testid="stButton"] > button,
        div[data-testid="stFormSubmitButton"] > button {
            border: none;
            border-radius: 16px;
            background: linear-gradient(135deg, #5767ff, #6f59ff 50%, #d95aa9);
            color: white;
            font-weight: 700;
            box-shadow: 0 12px 26px rgba(111, 89, 255, 0.18);
            min-height: 2.8rem;
        }

        div[data-testid="stButton"] > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            filter: brightness(1.03);
            transform: translateY(-1px);
        }

        [data-testid="stFileUploaderDropzone"] {
            border-radius: 20px !important;
            border: 1px dashed rgba(144, 156, 214, 0.42) !important;
            background: linear-gradient(180deg, #ffffff, #f8faff) !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            color: #405072 !important;
        }

        [data-testid="stFileUploaderDropzone"] button {
            background: linear-gradient(135deg, #eff3ff, #f7f5ff) !important;
            color: #33415f !important;
            border: 1px solid rgba(139, 150, 212, 0.32) !important;
            box-shadow: none !important;
            border-radius: 14px !important;
            font-weight: 700 !important;
        }

        [data-testid="stFileUploaderDropzone"] button:hover {
            background: linear-gradient(135deg, #e8eeff, #f2eeff) !important;
        }

        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div, .stFileUploader section {
            border-radius: 18px !important;
            border-color: rgba(211, 217, 236, 1) !important;
            background: rgba(255,255,255,0.98) !important;
            color: #1b2647 !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.94);
        }

        .stTextInput input,
        .stTextArea textarea,
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            color: #17233f !important;
            caret-color: #4f46e5 !important;
        }

        div[data-baseweb="input"],
        div[data-baseweb="textarea"],
        .stTextInput > div,
        .stTextArea > div,
        [data-testid="stChatInput"] {
            background: #ffffff !important;
            border-radius: 18px !important;
            box-shadow: none !important;
            overflow: hidden !important;
        }

        [data-testid="stChatInput"] {
            border: 1px solid rgba(213, 219, 237, 0.72) !important;
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: rgba(103, 114, 255, 0.28) !important;
            box-shadow: 0 0 0 1px rgba(103, 114, 255, 0.08) !important;
        }

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            border: none !important;
            box-shadow: none !important;
        }

        div[data-baseweb="textarea"] textarea {
            background: #ffffff !important;
            border-radius: 18px !important;
        }

        .stTextArea textarea:focus,
        .stTextInput input:focus,
        [data-testid="stChatInput"] textarea:focus,
        [data-testid="stChatInput"] input:focus {
            border-color: rgba(103, 114, 255, 0.36) !important;
            box-shadow: 0 0 0 1px rgba(103, 114, 255, 0.16) !important;
            outline: none !important;
        }

        [data-baseweb="tag"] {
            background: linear-gradient(135deg, rgba(95, 111, 255, 0.08), rgba(49, 196, 224, 0.08)) !important;
            border: 1px solid rgba(126, 140, 220, 0.16) !important;
            color: #24304f !important;
        }

        [data-baseweb="tag"] span,
        [data-baseweb="tag"] svg {
            color: #24304f !important;
            fill: #24304f !important;
        }

        .stTextArea textarea {
            min-height: 120px;
        }

        label[data-testid="stWidgetLabel"],
        label[data-testid="stWidgetLabel"] p,
        .stSelectbox label,
        .stTextInput label,
        .stTextArea label,
        .stMultiSelect label,
        .stFileUploader label {
            color: #22304d !important;
            font-weight: 700 !important;
        }

        [data-testid="stCaptionContainer"], .stCaption {
            color: #58657f !important;
        }

        [data-testid="stChatMessage"] {
            background: rgba(255,255,255,0.98);
            border: 1px solid rgba(227,231,244,0.95);
            border-radius: 26px;
            padding: 0.95rem 1rem;
            box-shadow: 0 8px 18px rgba(113, 127, 255, 0.06);
            margin-bottom: 0.75rem;
        }

        details {
            border-radius: 16px;
            background: rgba(255,255,255,0.98);
            border: 1px solid rgba(227,231,244,0.95);
        }

        mark {
            background: rgba(99, 102, 241, 0.18);
            color: #1c2b53;
            padding: 0.08rem 0.22rem;
            border-radius: 0.35rem;
        }

        @media (max-width: 1080px) {
            .chat-shell {
                grid-template-columns: 1fr;
            }
            .metric-strip, .quick-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">File<span>Z</span></div>
            <div class="sidebar-brand-subtitle">
                企业知识库与智能客服工作台
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_hero(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="app-shell">
            <div class="page-hero">
                <div class="page-eyebrow">{eyebrow}</div>
                <div class="page-title">{title}</div>
                <p class="page-subtitle">{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
