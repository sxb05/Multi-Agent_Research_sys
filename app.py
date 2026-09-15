import streamlit as st

from src.pipelines.pipeline import research_pipeline


st.set_page_config(
    page_title="Multi-Agent Research System",
    layout="wide",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,600&family=Manrope:wght@400;500;600;700&display=swap');

        :root {
                --ink: var(--text-color, #1f2b2c);
                --muted: var(--secondary-text-color, #657472);
                --paper: var(--background-color, #f5f1e8);
                --panel: var(--secondary-background-color, #fffdf8);
                --line: var(--border-color, #d8dfd8);
                --teal: var(--primary-color, #287d78);
                --teal-dark: #1e625e;
                --gold: #b96f43;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                    --ink: var(--text-color, #edf3ef);
                    --muted: var(--secondary-text-color, #a8b8b3);
                    --paper: var(--background-color, #111a1b);
                    --panel: var(--secondary-background-color, #1b2828);
                    --line: var(--border-color, #354746);
                    --teal: var(--primary-color, #70c7ba);
                    --teal-dark: #a0ddd3;
                    --gold: #e0a06e;
            }
        }

        .stApp {
                background: var(--paper);
                color: var(--ink);
                color-scheme: light dark;
                font-family: 'Manrope', sans-serif;
        }

        [data-testid='stHeader'] { background: transparent; }
        [data-testid='stSidebar'] {
            background: var(--panel);
            border-right: 1px solid var(--line);
        }
        [data-testid='stSidebar'] > div:first-child { padding: 1.1rem 0.8rem; }

        .main .block-container {
            max-width: 1050px;
            min-height: 88vh;
            padding: 0 3rem 5rem;
        }

        .brand {
            color: var(--ink);
            font-size: 0.86rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 0.4rem 0.55rem 1.3rem;
            text-transform: uppercase;
        }
        .nav-item {
            border-radius: 5px;
            color: var(--muted);
            font-size: 0.84rem;
            margin: 0.15rem 0;
            padding: 0.62rem 0.55rem;
        }
        .nav-item.active {
            background: color-mix(in srgb, var(--teal) 13%, transparent);
            color: var(--ink);
        }
        .nav-heading {
            color: var(--muted);
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            margin: 1.7rem 0 0.55rem;
            padding: 0 0.55rem;
            text-transform: uppercase;
        }
        .workspace-heading {
            color: var(--ink);
            font-family: 'Literata', Georgia, serif;
            font-size: clamp(2.4rem, 4vw, 3.7rem);
            font-weight: 500;
            letter-spacing: 0;
            line-height: 1;
            margin: 0 0 1.4rem;
            text-align: center;
        }
        .prompt-hint {
            color: var(--muted);
            font-size: 0.82rem;
            margin: 0 0 0.75rem;
            text-align: center;
        }
        .prompt-action {
            color: var(--muted);
            font-size: 0.78rem;
            margin-top: 0.6rem;
            text-align: center;
        }
        .section-label {
            color: var(--ink);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .sidebar-note {
            border-top: 1px solid var(--line);
            color: var(--muted);
            font-size: 0.82rem;
            line-height: 1.55;
            margin-top: 1.5rem;
            padding-top: 1.25rem;
        }
        .metric-card {
            background: var(--panel);
            border: 1px solid var(--line);
            border-left: 4px solid var(--teal);
            padding: 1rem 1.15rem;
        }
        .metric-label {
            color: var(--muted);
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .metric-value {
            color: var(--ink);
            font-family: 'Literata', Georgia, serif;
            font-size: 1.45rem;
            margin-top: 0.25rem;
        }

            h1, h2, h3, p, label { font-family: 'Manrope', sans-serif; }
        h2, h3 { color: var(--ink); }
        [data-testid='stTextArea'] textarea {
            background: var(--panel);
            border: 1px solid var(--line);
                border-radius: 8px;
            color: var(--ink);
            min-height: 3rem;
            padding: 0.85rem 1.15rem;
            resize: none;
        }
        [data-testid='stSlider'] { background: var(--panel); color: var(--ink); }
        [data-testid='stTextArea'] textarea:focus {
            border-color: var(--teal);
            box-shadow: 0 0 0 1px var(--teal);
        }
        [data-testid='stTextArea'] textarea::placeholder { color: var(--muted); }
        .stButton > button, .stDownloadButton > button {
            background: var(--panel);
            border-color: var(--line);
            color: var(--ink);
            border-radius: 3px;
            font-weight: 700;
            min-height: 2.75rem;
        }
        .stButton > button[kind='primary'] {
            background: var(--teal);
            border-color: var(--teal);
        }
        .stButton > button[kind='primary']:hover {
            background: var(--teal-dark);
            border-color: var(--teal-dark);
        }
        .stDownloadButton > button:hover {
            border-color: var(--teal);
            color: var(--teal);
        }
        [data-baseweb='tab-list'] { gap: 1.5rem; }
        [data-baseweb='tab'] { color: var(--muted); font-weight: 600; }
        [aria-selected='true'] { color: var(--teal) !important; }
        [data-testid='stAlert'] { border-radius: 3px; }
        @media (max-width: 640px) {
            .main .block-container { padding: 4rem 1.1rem 4rem; }
            .workspace-heading { font-size: 2.6rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

prompt_left, prompt_center, prompt_right = st.columns([1, 2, 1])
with prompt_center:
    st.markdown('<div class="workspace-heading">What should we focus on?</div>', unsafe_allow_html=True)
    st.markdown('<div class="prompt-hint">Search, synthesize, and review evidence in one workspace.</div>', unsafe_allow_html=True)
    topic = st.text_area(
        "Research question",
        placeholder="e.g. How are cities adapting to extreme heat?",
        height=120,
        label_visibility="collapsed",
    )

with st.sidebar:
    st.markdown('<div class="brand">Research lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item active">New research</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">Source library</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item">Saved reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-heading">Settings</div>', unsafe_allow_html=True)
    st.caption("Set the depth of your investigation.")

    num_results = st.slider(
        "Number of search results",
        min_value=1,
        max_value=10,
        value=5,
    )

    st.markdown(
        '<div class="sidebar-note">The pipeline finds relevant sources, extracts their content, drafts a report, and checks it for weaknesses.</div>',
        unsafe_allow_html=True,
    )

with prompt_center:
    run_research = st.button(
        "Start research",
        type="primary",
        use_container_width=True,
    )
    st.markdown('<div class="prompt-action">Your question stays private to this session.</div>', unsafe_allow_html=True)

if run_research:
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    try:
        with st.spinner("Running research pipeline..."):
            results = research_pipeline(
                topic=topic.strip(),
                num_results=num_results,
            )

        st.success("Research complete")

        metric_one, metric_two = st.columns(2)
        with metric_one:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Sources requested</div><div class="metric-value">{num_results}</div></div>',
                unsafe_allow_html=True,
            )
        with metric_two:
            st.markdown(
                '<div class="metric-card"><div class="metric-label">Review status</div><div class="metric-value">Critique included</div></div>',
                unsafe_allow_html=True,
            )

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Sources",
                "Notes",
                "Report",
                "Review",
            ]
        )

        with tab1:
            st.subheader("Source overview")
            st.markdown(results["search_results"])

        with tab2:
            st.subheader("Collected notes")
            st.markdown(results["scraped_content"])

        with tab3:
            st.subheader("Research report")
            st.markdown(results["report"])

            st.download_button(
                "Download report",
                data=results["report"],
                file_name="research_report.md",
                mime="text/markdown",
            )

        with tab4:
            st.subheader("Critical review")
            st.markdown(results["critique"])

    except Exception as error:
        st.error(f"Pipeline failed: {error}")
        st.exception(error)
else:
    st.info("Add a topic in the research brief to begin.")