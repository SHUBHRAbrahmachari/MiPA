from langchain_core.messages import AIMessage


def extract_ai_message_content(message: AIMessage):
    content = message.content
    print(content)
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        for block in content:
            if block.get("text") is not None:
                return block.get("text")

    return ""
