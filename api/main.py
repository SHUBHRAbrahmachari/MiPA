from fastapi import FastAPI
from src.api.user_data_routes import user_router
from src.api.user_api_secrets_routes import user_secrets_router
from src.api.chat_api import chat_route, load_context


app = FastAPI(name="MiPa", debug=True, lifespan=load_context)

app.include_router(user_router)
app.include_router(user_secrets_router)
app.include_router(chat_route)
