"""HTTP face of the dialogue layer.

`POST /chat` returns both the reply and the action, so a client can drive the
base without re-parsing the sentence. Run with:

    uvicorn apps.api_server:app --reload
"""
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ModuleNotFoundError as error:  # pragma: no cover - import-time guard
    raise SystemExit(
        "The API needs fastapi and uvicorn: pip install fastapi uvicorn"
    ) from error

from llm.echo_agent import EchoAgent

app = FastAPI(title="Smart Car Dialogue API")
agent = EchoAgent()


class ChatIn(BaseModel):
    text: str


@app.post("/chat")
def chat(inbox: ChatIn):
    return agent.respond(inbox.text)
