from src.database.checkpointers.checkpointer_factory import CheckpointerFactory
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient
from dotenv import load_dotenv
from typing_extensions import override
import os


class MongoDBCheckpointerFactory(CheckpointerFactory):
    def __init__(self):
        load_dotenv(
            dotenv_path=".env",
            verbose=False
        )

        self.__client = MongoClient(
            host=os.getenv("MONGO_CONNECTION_URL")
        )

        self.__checkpointer = MongoDBSaver(
            client=self.__client,
            db_name="mipa_checkpointing_db"
        )

    @override
    def load_checkpointer(self):
        return self.__checkpointer
