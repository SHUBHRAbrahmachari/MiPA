from src.database.secrets.user_secret_repository import UserSecretsRepository
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing_extensions import override
from dotenv import load_dotenv
import os


class UserSecretsMongoRepository(UserSecretsRepository):
    def __init__(self):
        super().__init__()
        load_dotenv(
            dotenv_path=".env",
            verbose=False
        )

        self._client = MongoClient(
            host=os.getenv("MONGO_CONNECTION_URL")
        )

        self._collection = self._client.user_secrets.user_api_keys
        self._collection.create_index(
            keys="username",
            unique=True
        )

    # USER CAN ADD API KEYS FOR EVERY UNIQUE API PROVIDERS LIKE OpenAI, Gemini, Anthropic etc
    @override
    def add_or_update_key(self, username: str, key_name: str, key: str) -> bool:
        try:
            self._collection.update_one(
                filter={
                    "username": username
                },
                update={
                    "$set": {
                        f"api_keys.{key_name}": key
                    }
                },
                upsert=True
            )
            return True

        except PyMongoError as e:
            print(str(e))
            return False

        except Exception as e:
            print(str(e))
            return False

    # TO FETCH API KEY REGARDING ANY LLM SERVICE PROVIDER
    @override
    def find_key(self, username: str, key_name: str) -> str | None:
        try:
            document = self._collection.find_one(
                filter={
                    "username": username
                }
            )

            if document is None:
                return None

            return document.get("api_keys", {}).get(key_name, None)

        except PyMongoError as e:
            print(str(e))
            return None

        except Exception as e:
            print(str(e))
            return None
