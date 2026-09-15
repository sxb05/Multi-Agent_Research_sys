from src.agents.agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain


def research_pipeline(topic: str, num_results: int = 5):
    """
    A research pipeline that searches the web for a given topic, scrapes the content of the top results,
    generates a report based on the scraped content, and then critiques the generated report.

    Args:
        topic (str): The topic to research.
        num_results (int): The number of search results to consider for scraping. Default is 5."""

    state = {}

    print("\n"+"="*50)
    print(f"Starting research pipeline for topic: {topic}")
    print ("\n"+"="*50)


    # Step 1: Search the web for the topic

    search_agent = build_search_agent()
    search_results = search_agent.invoke({"messages" : [("user", f"Find recent, relevant information on the topic: {topic}. Please provide the top {num_results} results with their URLs.")]

    })
    state["search_results"] = search_results["messages"][-1].content

    print("/n search results:", state["search_results"])


    #2 Step 2: Scrape the content of the top search results
    reader_agent = build_scrape_agent()
    reader_result = reader_agent.invoke({"messages" : [("user", f"Scrape the content of the following URLs: {state['search_results']}")]
                                         
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\n"+"="*50)
    print("Scraped content:", state["scraped_content"])


    #3 Step 3: Generate a report based on the scraped content
    research_combined = f"Research topic: {topic}\n\nScraped content:\n{state['scraped_content']}"
    report = writer_chain.invoke({"topic": topic, "information": research_combined})["output"]
    state["report"] = report    
    print("\n"+"="*50)
    print("Generated report:", state["report"])

    #4 Step 4: Critique the generated report
    critique = critic_chain.invoke({"report": state["report"]})["output"]
    state["critique"] = critique
    print("\n"+"="*50)
    print("Critique of the report:", state["critique"])

    return state