from pydantic import BaseModel, Field
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import Annotated


class ChatState(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str = Field(default="")
