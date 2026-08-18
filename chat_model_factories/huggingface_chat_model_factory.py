from src.chat_model_factories.chat_model_factory import ChatModelFactory
from src.chat_models.chat_model import ChatModel
from src.chat_models.huggingface_chat_model import HuggingFaceChatModel
from typing_extensions import override
import warnings

warnings.filterwarnings(action="ignore")

class HuggingFaceChatModelFactory(ChatModelFactory):
    @override
    def load_chat_model(self, model_name: str, api_key: str) -> ChatModel:
        model = HuggingFaceChatModel(
            model_name=model_name,
            api_key=api_key
        )

        return model
