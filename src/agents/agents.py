import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from ..tools.tools import web_search, scrape_webpage

load_dotenv()
GEMINI_3_8_KEY = os.environ.get("GEMINI_3_8_KEY")

llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        google_api_key = GEMINI_3_8_KEY,
        temperature=0.2,
        max_retries=3,
    )
llm2 = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0,
)
#First agent that can search the web and scrape content from a webpage
def build_search_agent():
    return create_agent(
        model=llm,
        tools = [web_search],
    )


#Second agent that can scrape content from a webpage
def build_scrape_agent():
    return create_agent(
        model=llm,
        tools = [scrape_webpage],
    )


writer_agent_prompt = ChatPromptTemplate.from_messages(
    [("system",


       """You are an expert reasearch writer that can write clear, well structured and insightful Reports. You will be given a topic and some information
    and your task is to write a coherent and informative piece of content based on that information. 
    Please ensure that the content is well-structured, clear, and concise. Avoid adding any information that is not provided in the input."""),




    ("human", """Write a report on the following 
    topic: 
    {topic} 
    using the following information: 
    {information}

    Structure the report with an introduction, key findings(minimum 3 well-explained points), and conclusion. Ensure that the content is well-organized and easy to read. Avoid adding any information that is not provided in the input.
    be professional and use a formal tone. Ensure that the content is well-structured, clear, and concise. Avoid adding any information that is not provided in the input.""")])


writer_chain = writer_agent_prompt | llm | StrOutputParser()



critic_agent_prompt = ChatPromptTemplate.from_messages(
    [("system", "You are an expert research critic that can critically analyze and evaluate the quality, accuracy, and relevance of a given report. Your task is to provide constructive feedback on the report, highlighting its strengths and weaknesses. Please ensure that your feedback is clear, concise, and actionable. Avoid adding any information that is not provided in the input."),
    ("human", """Critically analyze and evaluate the following report:  

    Score the report on a scale of 1 to 10, with 10 being the highest quality. Provide a detailed explanation for your score, highlighting the strengths and weaknesses of the report. Ensure that your feedback is clear, concise, and actionable. Avoid adding any information that is not provided in the input.
    report:
    {report}""")])


critic_chain = critic_agent_prompt | llm | StrOutputParser()