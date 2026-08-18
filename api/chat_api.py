from fastapi import APIRouter, FastAPI, Request
from fastapi import Depends, status, HTTPException
from contextlib import asynccontextmanager
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from src.context_manager.mipa_context_manager import context_manager
from src.api.jwt_decode import extract_username
from src.DTO.prompt_body import PromptBody
from src.exceptions.custom_exceptions import ApiKeyNotFoundException, ModelProviderNotSupportedException
from src.utility.ai_message_extraction import extract_ai_message_content

chat_route = APIRouter(
    tags=["chat"]
)


@asynccontextmanager
async def load_context(app: FastAPI):
    # LOAD THE CHATBOT TO FASTAPI'S STATE OBJECT
    app.state.chatbot = await context_manager.load_chatbot()
    yield
    # WRAP UP


@chat_route.post("/mipa/api/chat")
async def chat(prompt_body: PromptBody, request: Request, username: str = Depends(extract_username)) -> dict:
    chat_model_provider: str = prompt_body.chat_model_provider
    chat_model_name: str = prompt_body.chat_model_name
    prompt: str = prompt_body.prompt

    try:
        chat_model = await context_manager.load_chat_model(username, chat_model_provider, chat_model_name)

        config = RunnableConfig(
            configurable={
                "thread_id": username,
                "username": username,
                "chat_model": chat_model
            }
        )

        chatbot: CompiledStateGraph = request.app.state.chatbot

        response = await chatbot.ainvoke({
            "messages": [HumanMessage(content=prompt)]
        }, config=config
        )

        messages = response.get("messages")
        last_message = messages[-1]
        response = extract_ai_message_content(last_message)

        return {
            "status": "OK",
            "message": response
        }

    except ApiKeyNotFoundException as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "ERROR",
                "message": str(e)
            }
        )

    except ModelProviderNotSupportedException as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "ERROR",
                "message": str(e)
            }
        )

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "ERROR",
                "message": "something went wrong"
            }
        )
