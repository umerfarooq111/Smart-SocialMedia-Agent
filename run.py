from langchain_core.messages import HumanMessage
from app.agent.agent import agent
from app.utils.helpers import extract_text

def main():

    print("=" * 60)
    print("AI Social Media Moderation Agent")
    print("=" * 60)

    while True:

        comment = input("\nEnter Comment (type 'exit' to quit):\n> ")

        if comment.lower() == "exit":
            break

        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=comment)
                ]
            }
        )

        print("\n" + "=" * 60)
        print("Final Response")
        print("=" * 60)


        print(extract_text(result["messages"][-1]))

if __name__ == "__main__":
    main()