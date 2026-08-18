from src.chat_models.chat_model import ChatModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing_extensions import override
import warnings

warnings.filterwarnings(action="ignore")


class OpenAIChatModel(ChatModel):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name, api_key)

        self.__model = ChatOpenAI(
            model=self._model_name,
            api_key=self._api_key
        )

    @override
    def invoke(self, prompt: list[BaseMessage] | HumanMessage) -> AIMessage:
        response = self.__model.invoke(prompt)
        return response

    @override
    async def ainvoke(self, prompt: list[BaseMessage] | HumanMessage) -> AIMessage:
        response = await self.__model.ainvoke(prompt)
        return response
