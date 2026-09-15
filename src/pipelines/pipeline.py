from src.agents.agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain


def research_pipeline(topic: str, num_results: int = 5):
    """
    A research pipeline that searches the web for a given topic, scrapes the content of the top results,
    generates a report based on the scraped content, and then critiques the generated report.

    Args:
        topic (str): The topic to research.
        num_results (int): The number of search results to consider for scraping. Default is 5.
    """

    state = {}

    print("\n" + "=" * 50)
    print(f"Starting research pipeline for topic: {topic}")
    print("\n" + "=" * 50)

    # Helper function to extract text cleanly from structured Gemini/LangChain message blocks
    def extract_clean_text(message_content):
        if isinstance(message_content, list):
            extracted = []
            for item in message_content:
                if isinstance(item, dict) and "text" in item:
                    extracted.append(item["text"])
            return "\n".join(extracted)
        return str(message_content)

    # Step 1: Search the web for the topic
    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, relevant information on the topic: {topic}. Please provide the top {num_results} results with their URLs.")
        ]
    })
    
    # FIXED: Convert the structured list of blocks into a clean raw string
    state["search_results"] = extract_clean_text(search_results["messages"][-1].content)
    print("\n[+] Cleaned search results loaded into state.")

    # Step 2: Scrape the content of the top search results
    reader_agent = build_scrape_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            ("user", f"Scrape the content of the following URLs: {state['search_results']}")
        ]
    })

    # FIXED: Convert the structured list of blocks into a clean raw string
    state["scraped_content"] = extract_clean_text(reader_result["messages"][-1].content)
    print("\n" + "=" * 50)
    print("[+] Cleaned scraped content loaded into state.")

    # Step 3: Generate a report based on the scraped content
    research_combined = f"Research topic: {topic}\n\nScraped content:\n{state['scraped_content']}"
    
    print("\n" + "=" * 50)
    print("Generating report...")
    # FIXED: Invoke without trailing ['output'] for modern LCEL compatibility
    report = writer_chain.invoke({"topic": topic, "information": research_combined})
    state["report"] = report    
    print("\nGenerated report:\n", state["report"])

    # Step 4: Critique the generated report
    print("\n" + "=" * 50)
    print("Critiquing report...")
    # FIXED: Invoke without trailing ['output'] for modern LCEL compatibility
    critique = critic_chain.invoke({"report": state["report"]})
    state["critique"] = critique
    print("\nCritique of the report:\n", state["critique"])

    return state



                                                                                                                                        # from src.agents.agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain


                                                                                                                                        # def research_pipeline(topic: str, num_results: int = 5):
                                                                                                                                        #     """
                                                                                                                                        #     A research pipeline that searches the web for a given topic, scrapes the content of the top results,
                                                                                                                                        #     generates a report based on the scraped content, and then critiques the generated report.

                                                                                                                                        #     Args:
                                                                                                                                        #         topic (str): The topic to research.
                                                                                                                                        #         num_results (int): The number of search results to consider for scraping. Default is 5."""

                                                                                                                                        #     state = {}

                                                                                                                                        #     print("\n"+"="*50)
                                                                                                                                        #     print(f"Starting research pipeline for topic: {topic}")
                                                                                                                                        #     print ("\n"+"="*50)


                                                                                                                                        #     # Step 1: Search the web for the topic

                                                                                                                                        #     search_agent = build_search_agent()
                                                                                                                                        #     search_results = search_agent.invoke({"messages" : [("user", f"Find recent, relevant information on the topic: {topic}. Please provide the top {num_results} results with their URLs.")]

                                                                                                                                        #     })
                                                                                                                                        #     state["search_results"] = search_results["messages"][-1].content

                                                                                                                                        #     print("/n search results:", state["search_results"])


                                                                                                                                        #     #2 Step 2: Scrape the content of the top search results
                                                                                                                                        #     reader_agent = build_scrape_agent()
                                                                                                                                        #     reader_result = reader_agent.invoke({"messages" : [("user", f"Scrape the content of the following URLs: {state['search_results']}")]
                                                                                                                                                                                
                                                                                                                                        #     })

                                                                                                                                        #     state["scraped_content"] = reader_result["messages"][-1].content

                                                                                                                                        #     print("\n"+"="*50)
                                                                                                                                        #     print("Scraped content:", state["scraped_content"])


                                                                                                                                        #     #3 Step 3: Generate a report based on the scraped content
                                                                                                                                        #     research_combined = f"Research topic: {topic}\n\nScraped content:\n{state['scraped_content']}"
                                                                                                                                        #     report = writer_chain.invoke({"topic": topic, "information": research_combined})
                                                                                                                                        #     state["report"] = report    
                                                                                                                                        #     print("\n"+"="*50)
                                                                                                                                        #     print("Generated report:", state["report"])

                                                                                                                                        #     #4 Step 4: Critique the generated report
                                                                                                                                        #     critique = critic_chain.invoke({"report": state["report"]})
                                                                                                                                        #     state["critique"] = critique
                                                                                                                                        #     print("\n"+"="*50)
                                                                                                                                        #     print("Critique of the report:", state["critique"])

                                                                                                                                        #     return state