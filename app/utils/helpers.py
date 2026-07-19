def extract_text(message):

    if isinstance(message.content, str):
        return message.content

    if isinstance(message.content, list):
        texts = []

        for block in message.content:
            if block.get("type") == "text":
                texts.append(block["text"])

        return "\n".join(texts)

    return str(message.content)