from src.chat_model_factories.chat_model_factory import ChatModelFactory
from src.chat_models.chat_model import ChatModel
from src.chat_models.anthropic_chat_model import AnthropicChatModel
from typing_extensions import override
import warnings

warnings.filterwarnings(action="ignore")

class AnthropicChatModelFactory(ChatModelFactory):
    @override
    def load_chat_model(self, model_name: str, api_key: str) -> ChatModel:
        model = AnthropicChatModel(
            model_name=model_name,
            api_key=api_key
        )

        return model
