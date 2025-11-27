# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from agent import agent_response

app = FastAPI(title="AI Question-Answer Helper (Simple)")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "AI Question-Answer Helper. Use POST /chat with JSON {\"message\": \"...\"}"}

@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    """
    POST /chat
    Body JSON: {"message": "<text>"}
    Response JSON: {"type": "...", "answer": "...", "memory": [...]}
    """
    resp = agent_response(req.message)
    return resp
