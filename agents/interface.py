"""
Interface Agent (Router) - This file CREATES the Interface/Router Agent.

This is where the Interface Agent is defined with its:
- Specialized system prompt (defines the agent's "personality" as a classifier)
- LLM connection
- State processing logic
- Router decision function

The agent is then connected to the graph in graph.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))

def interface_llm(state):
    """
    Interface Agent Function - This CREATES the Router/Classifier Agent.
    
    This function defines:
    1. The agent's specialized prompt (classification expertise)
    2. How it processes incoming state
    3. How it generates classification responses using the LLM
    
    This agent is then connected to the graph in graph.py using:
    graph_builder.add_node("interface_node", interface_llm)
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a customer care bot, tell me whether the given problem is based on Billing Issue, Technical Issue, or Feedback."),
            ("user", "issue: {issue}")
        ]
    )
    chain = prompt|llm
    user_msg = state["messages"][-1].content
    response = chain.invoke({"issue": user_msg})
    return {"messages": state["messages"] + [response]}


def router_decision(state) :
    classification = state["messages"][-1].content.lower().strip()

    if "billing" in classification:
        return "billing_node"
    elif "technical" in classification:
        return "technical_node"
    elif "feedback" in classification:
        return "feedback_node"
    else:
        return "feedback_node"