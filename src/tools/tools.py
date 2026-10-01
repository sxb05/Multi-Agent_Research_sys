import os
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_tavily import TavilySearch
import trafilatura

load_dotenv()
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
search_tool = TavilySearch(max_results=5, apikey=TAVILY_API_KEY)

@tool
def scrape_webpage(url: str) -> str:
    """
    Scrape the content of a webpage given its URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: The scraped content of the webpage.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com",
        }
    try:

        # response = requests.get(url, headers=headers, timeout=10)
        # response.raise_for_status()  # Raise an error for bad responses

        # # Use BeautifulSoup to parse the HTML content
        # soup = BeautifulSoup(response.content, 'html.parser')

        # # Use readability-lxml to extract the main content
        # doc = Document(response.text)
        # main_content = doc.summary()

        # # Clean up the text using trafilatura
        # cleaned_content = trafilatura.extract(main_content)

        # return cleaned_content if cleaned_content else "No content could be extracted."

    
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  

        # Let trafilatura handle everything natively from the raw code
        cleaned_content = trafilatura.extract(response.text)

        return cleaned_content if cleaned_content else "No content could be extracted."

    except Exception as e:
        return f"An error occurred while scraping the webpage: {e}"



@tool
def web_search(query: str) -> str:
    """
    Perform a web search using the Tavily API and return the results.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    try:
        results = search_tool.run(query)
        out = []
        
        # Tavily returns a dictionary; the list of results is inside the 'results' key
        search_results_list = results.get('results', [])
        
        for r in search_results_list:
            out.append(f"Title: {r.get('title')}\nURL: {r.get('url')}\nContent: {r.get('content', '')[:400]}\n")
            
        return "\n\n".join(out)
    except Exception as e:
        return f"An error occurred while performing the web search: {e}"