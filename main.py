"""
FastAPI server for the AgenticAI Support Bot.

Exposes a REST API that accepts customer inquiries and routes them
through the LangGraph workflow to specialized agents.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from graph import graph
load_dotenv()

app = FastAPI(title="AgenticAI Support Bot")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def root():
    """Health check endpoint."""
    return {"message" : "Welcome to AgenticAI Support Bot API"}

@app.post("/chat")
def chat(request: MessageRequest):
    """
    Main chat endpoint that processes customer inquiries.
    
    Routes the message through the LangGraph workflow and returns
    both the classification and the final agent response.
    """
    # Invoke the graph with the user's message
    response = graph.invoke({"messages": request.message})
    messages = response["messages"]

    # Extract classification (from interface_node) and final response (from specialist)
    classification = messages[-2].content
    final_response = messages[-1].content

    return {
        "classification": classification,
        "response": final_response
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)