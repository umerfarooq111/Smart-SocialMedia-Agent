from langchain_core.messages import HumanMessage
from app.agent.agent import agent
from app.utils.printer import print_stream

def main():

    print("=" * 60)
    print("AI Social Media Moderation Agent")
    print("=" * 60)

    while True:

        comment = input("\nEnter Comment (type 'exit' to quit):\n> ")

        if comment.lower() == "exit":
            break

        print("\n" + "=" * 60)
        print("Agent Streaming Progress")
        print("=" * 60)

        for chunk in agent.stream(
            {
                "messages": [
                    HumanMessage(content=comment)
                ]
            }
        ):
            print_stream(chunk)

        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()