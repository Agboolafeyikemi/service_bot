"""
Feedback Agent - This file CREATES the Feedback Support Agent.

This is where the Feedback Agent is defined with its:
- Specialized system prompt (defines the agent's "personality")
- LLM connection
- State processing logic

The agent is then connected to the graph in graph.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

def feedback_llm(state):
    """
    Feedback Agent Function - This CREATES the Feedback Support Agent.
    
    This function defines:
    1. The agent's specialized prompt (feedback handling expertise)
    2. How it processes incoming state
    3. How it generates responses using the LLM
    
    This agent is then connected to the graph in graph.py using:
    graph_builder.add_node("feedback_node", feedback_llm)
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you are a feedback bot, thank the user for their feedback and assure them that their feedback is valuable."),
            ("user", "issue: {issue}")
        ]
    )
    chain = prompt|llm
    user_msg = state["messages"][-2].content
    response = chain.invoke({"issue": user_msg})
    return {"messages": state["messages"] + [response]}