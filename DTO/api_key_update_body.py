from pydantic import BaseModel
from typing import Literal


class APIKeyUpdateBody(BaseModel):
    provider_name: Literal["anthropic", "google", "openai", "huggingface", "openrouter"]
    api_key: str
