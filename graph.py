"""
LangGraph workflow for multi-agent customer service bot.

This graph implements a router pattern:
1. All requests start at the interface_node (router)
2. Router classifies the inquiry and routes to appropriate specialist
3. Specialist agent handles the request and returns response
4. Technical agent can use web_search tool for troubleshooting
"""
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from agents.interface import interface_llm, router_decision
from agents.billing import billing_llm
from agents.technical import technical_llm, web_search
from agents.feedback import feedback_llm
import os

class State(TypedDict):
    messages : Annotated[list, add_messages]

def create_graph():
    """Creates and compiles the LangGraph workflow."""
    graph_builder = StateGraph(State)

    # Add specialized agent nodes
    graph_builder.add_node("interface_node", interface_llm)  # Router/classifier
    graph_builder.add_node("billing_node", billing_llm)
    graph_builder.add_node("technical_node", technical_llm)
    graph_builder.add_node("feedback_node", feedback_llm)
    
    # Add tool node for technical agent (web_search)
    graph_builder.add_node("technical_tool_node", ToolNode([web_search]))

    # Define workflow edges
    graph_builder.add_edge(START, "interface_node")  # All requests start here
    
    # Conditional routing based on classification
    graph_builder.add_conditional_edges(
        "interface_node",
        router_decision,  # Decision function determines next node
        {
            "billing_node": "billing_node",
            "technical_node": "technical_node",
            "feedback_node": "feedback_node"
        }
    )
    
    # Billing and Feedback nodes end the workflow
    graph_builder.add_edge("billing_node", END)
    graph_builder.add_edge("feedback_node", END)
    
    # Technical node can call tools, so we need conditional routing
    graph_builder.add_conditional_edges(
        "technical_node",
        tools_condition,  # Check if agent wants to call a tool
        {
            "tools": "technical_tool_node",  # If tool call, go to tool node
            "__end__": END  # If no tool call, end workflow
        }
    )
    
    # After tool execution, return to technical agent
    graph_builder.add_edge("technical_tool_node", "technical_node")

    return graph_builder.compile()

graph = create_graph()