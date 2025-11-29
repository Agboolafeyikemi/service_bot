"""
Technical Agent - This file CREATES the Technical Support Agent.

This is where the Technical Agent is defined with its:
- Specialized system prompt (defines the agent's "personality")
- LLM connection
- State processing logic
- Web search tool for troubleshooting

The agent is then connected to the graph in graph.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

# Create web search tool for troubleshooting
tavily_tool = TavilySearch(max_results=3)

@tool
def web_search(query: str) -> str:
    """
    Search the web for troubleshooting issues and technical solutions.
    
    Use this tool when you need to find:
    - Recent solutions to technical problems
    - Troubleshooting guides
    - Error message explanations
    - Technical documentation
    
    Args:
        query: The search query for troubleshooting the technical issue
        
    Returns:
        Search results with relevant information
    """
    return tavily_tool.invoke(query)

# Bind tools to the LLM
llm_with_tools = llm.bind_tools([web_search])

def technical_llm(state):
    """
    Technical Agent Function - This CREATES the Technical Support Agent.
    
    This function defines:
    1. The agent's specialized prompt (technical support expertise)
    2. How it processes incoming state
    3. How it generates responses using the LLM
    4. Access to web_search tool for finding solutions
    
    This agent is then connected to the graph in graph.py using:
    graph_builder.add_node("technical_node", technical_llm)
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
             "You are a technical support bot. Help users with their technical issues. "
             "You have access to a web_search tool that you can use to find recent solutions, "
             "troubleshooting guides, and technical documentation. Use the web_search tool when "
             "you need to find up-to-date information about technical problems or error messages."),
            ("user", "issue: {issue}")
        ]
    )
    chain = prompt | llm_with_tools
    user_msg = state["messages"][-2].content
    response = chain.invoke({"issue": user_msg})
    return {"messages": state["messages"] + [response]}