from abc import ABC, abstractmethod
from src.chat_models.chat_model import ChatModel


class ChatModelFactory(ABC):
    @abstractmethod
    def load_chat_model(self, model_name: str, api_key: str) -> ChatModel:
        pass
