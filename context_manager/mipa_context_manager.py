from langgraph.graph.state import CompiledStateGraph
from src.chat_model_factories.chat_model_factory import ChatModelFactory
from src.chat_model_factories.google_chat_model_factory import GoogleChatModelFactory
from src.chat_model_factories.anthropic_chat_model_factory import AnthropicChatModelFactory
from src.chat_model_factories.huggingface_chat_model_factory import HuggingFaceChatModelFactory
from src.chat_model_factories.openai_chat_model_factory import OpenAIChatModelFactory
from src.chat_model_factories.openrouter_chat_model_factory import OpenRouterChatModelFactory
from src.exceptions.custom_exceptions import ModelProviderNotSupportedException, ApiKeyNotFoundException
from src.database.users.user_repository import UserRepository
from src.database.users.supabase_user_repository import SupabaseUserRepository
from src.database.secrets.user_secret_repository import UserSecretsRepository
from src.database.secrets.user_secret_mongo_repository import UserSecretsMongoRepository
from src.security.password_encoder import PasswordEncoder
from src.security.bcrypt_password_encoder import BcryptPasswordEncoder
from src.security.jwt_secret_manager import JwtSecurityManager
from src.database.checkpointers.checkpointer_factory import CheckpointerFactory
from src.database.checkpointers.mongodb_checkpointer_factory import MongoDBCheckpointerFactory
from src.chat_models.chat_model import ChatModel
from src.workflow.chatbot_workflow import load_chatbot
import json


# THE CENTRAL APPLICATION CONTEXT PRESERVER
class MipaApplicationContext:
    def __init__(self):
        # CREATE APPLICATION DEPENDENCIES
        self.__password_encoder: PasswordEncoder = BcryptPasswordEncoder()
        self.__user_repository: UserRepository = SupabaseUserRepository(self.__password_encoder)
        self.__user_secrets_repository: UserSecretsRepository = UserSecretsMongoRepository()
        self.__security_manager: JwtSecurityManager = JwtSecurityManager(self.__user_repository)
        self.__checkpointer_factory: CheckpointerFactory = MongoDBCheckpointerFactory()

        # LOAD THE CONFIGURATION
        with open("config.json", "r") as file:
            self.__config = json.load(file)

        # LOAD THE SUPPORTED MODEL PROVIDERS
        self.__model_providers = frozenset(self.__config.get("model_providers"))

        # LOAD PROVIDER TO MODEL API KEY NAMES
        self.__provider_to_model_api_key_names = self.__config.get("provider_to_api_key_mapping")

        # FOR MODEL CACHING AGAINST USERS
        self.__chat_models: dict[str, dict[str, ChatModel]] = {}

        # GET THE CHAT MODEL FACTORIES
        self.__chat_model_factories: dict[str, ChatModelFactory] = {
            "google": GoogleChatModelFactory(),
            "anthropic": AnthropicChatModelFactory(),
            "openai": OpenAIChatModelFactory(),
            "huggingface": HuggingFaceChatModelFactory(),
            "openrouter": OpenRouterChatModelFactory()
        }

    def get_user_repository(self) -> UserRepository:
        return self.__user_repository

    def get_user_secrets_repository(self) -> UserSecretsRepository:
        return self.__user_secrets_repository

    def get_security_manager(self) -> JwtSecurityManager:
        return self.__security_manager

    def get_password_encoder(self) -> PasswordEncoder:
        return self.__password_encoder

    # TO LOAD THE CHATBOT BEFORE LAUNCHING THE SERVER
    async def load_chatbot(self) -> CompiledStateGraph:
        chatbot = await load_chatbot(self.__checkpointer_factory)
        return chatbot

    # TO LOAD AND CACHE CHAT MODELS AGAINST A USERNAME
    async def load_chat_model(self, username: str, model_provider: str, model_name: str) -> ChatModel:
        if model_provider not in self.__model_providers:
            raise ModelProviderNotSupportedException(f"model provider {model_provider} is not supported!")

        # LOOK IF THE MODEL EXISTS
        model_id = model_provider+":"+model_name

        chat_models = self.__chat_models
        if chat_models.get(username) is None or chat_models.get(username).get(model_id) is None:
            api_key_name = self.__provider_to_model_api_key_names.get(model_provider)
            api_key = self.__user_secrets_repository.find_key(username, api_key_name)

            if api_key is None:
                raise ApiKeyNotFoundException(f"API key for {model_provider} does not exist")

            chat_model: ChatModel = self.__chat_model_factories.get(model_provider).load_chat_model(
                model_name,
                api_key
            )

            if self.__chat_models.get(username) is None:
                self.__chat_models[username] = {model_id: chat_model}

            if self.__chat_models.get(username).get(model_id) is None:
                self.__chat_models[username][model_id] = chat_model

        return self.__chat_models.get(username).get(model_id)


context_manager = MipaApplicationContext()
