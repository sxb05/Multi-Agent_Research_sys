import streamlit as st

from src.pipelines.pipeline import research_pipeline


st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Multi-Agent Research System")
st.write(
    "Search the web, scrape relevant sources, generate a report, "
    "and critique the result."
)

with st.sidebar:
    st.header("Research Settings")

    topic = st.text_area(
        "Research topic",
        placeholder="Example: Recent advances in artificial intelligence",
        height=120,
    )

    num_results = st.slider(
        "Number of search results",
        min_value=1,
        max_value=10,
        value=5,
    )

    run_research = st.button(
        "Run Research Pipeline",
        type="primary",
        use_container_width=True,
    )

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

        st.success("Research completed successfully.")

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "Search Results",
                "Scraped Content",
                "Generated Report",
                "Critique",
            ]
        )

        with tab1:
            st.subheader("Search Results")
            st.markdown(results["search_results"])

        with tab2:
            st.subheader("Scraped Content")
            st.markdown(results["scraped_content"])

        with tab3:
            st.subheader("Generated Report")
            st.markdown(results["report"])

            st.download_button(
                "Download Report",
                data=results["report"],
                file_name="research_report.md",
                mime="text/markdown",
            )

        with tab4:
            st.subheader("Critique")
            st.markdown(results["critique"])

    except Exception as error:
        st.error(f"Pipeline failed: {error}")
        st.exception(error)
else:
    st.info("Enter a topic and click **Run Research Pipeline**.")