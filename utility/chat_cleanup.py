from src.utility.summary_generation import generate_summary
from src.chat_models.chat_model import ChatModel
from langchain_core.messages import RemoveMessage, trim_messages
from langchain_core.messages import BaseMessage
import json


def cleanup_chat(chat_model: ChatModel, messages: list[BaseMessage], previous_summary: str = ""):
    with open("config.json", "r") as f:
        config = json.load(f)

    found_messages = trim_messages(
        messages=messages,
        max_tokens=config.get("token_cleanup_trigger"),
        token_counter="approximate",
        strategy="last",
        allow_partial=False,
        include_system=False
    )

    if len(found_messages) == len(messages):
        return {
            "messages": messages,
            "summary": previous_summary
        }

    messages_to_keep = trim_messages(
        messages=messages,
        max_tokens=config.get("token_cleanup_target"),
        token_counter="approximate",
        strategy="last",
        allow_partial=False,
        include_system=False
    )

    ids_to_keep = {message.id for message in messages_to_keep}
    messages_to_remove = [message for message in messages if message.id not in ids_to_keep]
    summary = generate_summary(chat_model, messages_to_remove, previous_summary)

    new_messages = [RemoveMessage(id=message.id) for message in messages_to_remove]

    return {
        "messages": new_messages,
        "summary": summary
    }
