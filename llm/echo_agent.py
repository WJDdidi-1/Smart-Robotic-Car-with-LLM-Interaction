class EchoAgent:
    def __init__(self, system_prompt="You are a helpful robot."):
        self.system_prompt = system_prompt
    def chat(self, user_text: str) -> str:
        return f"[Robot]: I heard you say -> {user_text}"
