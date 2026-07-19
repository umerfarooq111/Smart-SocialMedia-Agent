from langchain_core.messages import AIMessage, ToolMessage


def print_stream(chunk):

    for node, data in chunk.items():

        print(f"\n[{node.upper()}]")

        if "messages" not in data:
            continue

        for message in data["messages"]:

            if isinstance(message, AIMessage):

                if message.content:
                    print(message.content)

                if message.tool_calls:
                    for tool in message.tool_calls:
                        print(f"\n🔧 Calling: {tool['name']}")

            elif isinstance(message, ToolMessage):

                print(f"✅ {message.content}")