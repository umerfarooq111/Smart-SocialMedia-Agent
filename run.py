from langchain_core.messages import HumanMessage
from app.agent.agent import agent
from app.utils.printer import print_stream

def main():
    print("=" * 60)
    print("AI Customer Support & Moderation Agent")
    print("=" * 60)

    user_id = input("\nEnter User ID (default: customer_001):\n> ").strip()
    if not user_id:
        user_id = "customer_001"

    print(f"\n[Session Started for User ID: {user_id}]")
    print("Commands: 'exit' to quit, 'switch' to change User ID\n")

    while True:
        comment = input(f"\n[{user_id}] Enter Message:\n> ").strip()

        if not comment:
            continue

        if comment.lower() == "exit":
            print("\nExiting session. Goodbye!")
            break

        if comment.lower() == "switch":
            new_id = input("\nEnter new User ID:\n> ").strip()
            if new_id:
                user_id = new_id
                print(f"\n[Switched to User ID: {user_id}]")
            continue

        print("\n" + "=" * 60)
        print("Agent Streaming Progress")
        print("=" * 60)

        final_message = None
        for chunk in agent.stream(
            {
                "messages": [
                    HumanMessage(content=comment)
                ]
            },
        ):
            print_stream(chunk)

            for _, data in chunk.items():
                if "messages" in data:
                    final_message = data["messages"][-1]

        print("\n" + "=" * 60)
        print("Final Response")
        print("=" * 60)

        if final_message:
            print(final_message.content)

if __name__ == "__main__":
    main()