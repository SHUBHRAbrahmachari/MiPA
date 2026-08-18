from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from src.chat_models.chat_model import ChatModel
from typing_extensions import override
import warnings

warnings.filterwarnings(action="ignore")


class AnthropicChatModel(ChatModel):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name, api_key)

        self.__model = ChatAnthropic(
            model_name=self._model_name,
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
