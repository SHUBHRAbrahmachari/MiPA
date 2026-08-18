from src.chat_model_factories.chat_model_factory import ChatModelFactory
from src.chat_models.chat_model import ChatModel
from src.chat_models.openrouter_chat_model import OpenRouterChatModel
from typing_extensions import override
import warnings

warnings.filterwarnings(action="ignore")


class OpenRouterChatModelFactory(ChatModelFactory):
    @override
    def load_chat_model(self, model_name: str, api_key: str) -> ChatModel:
        model = OpenRouterChatModel(
            model_name=model_name,
            api_key=api_key
        )

        return model
