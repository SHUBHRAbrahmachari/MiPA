from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class ChatModel(ABC):
    def __init__(self, model_name: str, api_key: str):
        self._model_name = model_name
        self._api_key = api_key

    def get_model_name(self):
        return self._model_name

    @abstractmethod
    def invoke(self, prompt: list[BaseMessage] | HumanMessage) -> AIMessage:
        pass

    @abstractmethod
    async def ainvoke(self, prompt: list[BaseMessage] | HumanMessage) -> AIMessage:
        pass
