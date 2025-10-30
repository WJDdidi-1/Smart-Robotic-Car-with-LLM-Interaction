from llm.echo_agent import EchoAgent
def main():
    agent = EchoAgent()
    print("Type something (q to quit):")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"q", "quit", "exit"}:
            break
        reply = agent.chat(user)
        print(reply)
if __name__ == "__main__":
    main()
