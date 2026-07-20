from langchain_core.messages import AIMessage


def print_stream(chunk):

    for _, data in chunk.items():

        if "messages" not in data:
            continue

        for message in data["messages"]:

            # Show only tool calls
            if isinstance(message, AIMessage):

                if message.tool_calls:
                    for tool in message.tool_calls:
                        print(f"\n🔧 Calling: {tool['name']}")