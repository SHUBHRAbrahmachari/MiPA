from pydantic import BaseModel


class PromptBody(BaseModel):
    chat_model_provider: str
    chat_model_name: str
    prompt: str
