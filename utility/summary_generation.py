from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from src.chat_models.chat_model import ChatModel
from src.utility.ai_message_extraction import extract_ai_message_content
from src.utility.summary_prompt_template import load_summary_generation_prompt_value


def generate_summary(chat_model: ChatModel, messages: list[BaseMessage], previous_summary: str = "") -> str:
    chat_messages = []
    for message in messages:
        if isinstance(message, HumanMessage):
            chat_messages.append(f"HUMAN : \n{message.content}")
        elif isinstance(message, AIMessage):
            chat_messages.append(f"AI: \n{extract_ai_message_content(message)}")
        else:
            continue

    chat = "\n\n".join(message for message in chat_messages)
    prompt_value = load_summary_generation_prompt_value(chat, previous_summary)
    content = chat_model.invoke(prompt_value)

    return extract_ai_message_content(content)
