from fastapi import FastAPI
from pydantic import BaseModel
from llm.echo_agent import EchoAgent
app = FastAPI(title="Smart Car Dialogue API")
agent = EchoAgent()
class ChatIn(BaseModel):
    text: str
@app.post("/chat")
def chat(inbox: ChatIn):
    return {"reply": agent.chat(inbox.text)}
