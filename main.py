from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from graph import graph
load_dotenv()

app = FastAPI(title="AgenticAI Support Bot")

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
    return {"message" : "Wellcome to AgenticAI Support Bot API"}

@app.post("/chat")
def chat(request: MessageRequest):

    response = graph.invoke({"messages": request.message})
    messages = response["messages"]

    classification = messages[-2].content
    final_response = messages[-1].content

    return {
        "classification": classification,
        "response": final_response
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)