from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from agents.interface import interface_llm, router_decision
from agents.billing import billing_llm
from agents.technical import technical_llm
from agents.feedback import feedback_llm
import os

class State(TypedDict):
    messages : Annotated[list, add_messages]

def create_graph():
    graph_builder = StateGraph(State)


    graph_builder.add_node("interface_node", interface_llm)
    graph_builder.add_node("billing_node", billing_llm)
    graph_builder.add_node("technical_node", technical_llm)
    graph_builder.add_node("feedback_node", feedback_llm)


    graph_builder.add_edge(START, "interface_node")
    graph_builder.add_conditional_edges(
        "interface_node",
        router_decision,
        {
            "billing_node": "billing_node",
            "technical_node": "technical_node",
            "feedback_node": "feedback_node"
        }
    )
    graph_builder.add_edge("billing_node", END)
    graph_builder.add_edge("technical_node", END)
    graph_builder.add_edge("feedback_node", END)

    return graph_builder.compile()

graph = create_graph()