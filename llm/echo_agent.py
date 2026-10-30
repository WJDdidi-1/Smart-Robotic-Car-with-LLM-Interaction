"""The dialogue layer, kept deliberately small.

It does two things: it turns the sentence into an action with the same parser
the controller obeys, and it writes a reply that names that action. Swapping
this for a real model means implementing `respond` with a tool call that
returns the same `Intent` shape — nothing downstream has to change.
"""
from intent.parser import parse


class EchoAgent:
    def __init__(self, system_prompt="You are a helpful robot."):
        self.system_prompt = system_prompt

    def respond(self, user_text: str) -> dict:
        intent = parse(user_text)
        if intent.action == "SMALLTALK":
            reply = f"[Robot]: I heard you say -> {user_text}"
        else:
            reply = f"[Robot]: {intent.action.lower().replace('_', ' ')}"
        return {"reply": reply, "action": intent.action, "args": intent.args}

    def chat(self, user_text: str) -> str:
        return self.respond(user_text)["reply"]
