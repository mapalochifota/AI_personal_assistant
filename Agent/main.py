from agent import Agent

def main():
    print("\n" + "=" * 50)
    print("     Personal AI Assistant")
    print("=" * 50)
    print("Type 'quit' to exit | 'history' to see memory\n")

    try:
        agent = Agent()
    except EnvironmentError as e:
        print(f"Setup error: {e}")
        return

    greeting = agent.chat("Greet the user warmly and list what you can help with.")
    print(f"Assistant: {greeting}\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "bye"):
                print("Assistant: Goodbye! Have a great day!")
                break

            if user_input.lower() == "history":
                print(agent.memory.summary())
                continue

            response = agent.chat(user_input)
            print(f"\nAssistant: {response}\n")

        except KeyboardInterrupt:
            print("\nAssistant: Goodbye!")
            break

if __name__ == "__main__":
    main()