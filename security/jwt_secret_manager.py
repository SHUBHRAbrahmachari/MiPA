from src.database.users.user_repository import UserRepository
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
import os
import json


class JwtSecurityManager:
    def __init__(self, repository: UserRepository):
        load_dotenv(
            dotenv_path=".env",
            verbose=False
        )

        self.__repository = repository
        with open("config.json", "r") as file:
            self.__json_configuration = json.load(file)

        self.__SECRET = os.getenv("SECRET")
        self.__DURATION = self.__json_configuration.get("jwt_duration_in_minutes")

    def generate_token(self, username: str) -> str:
        exp = datetime.now() + timedelta(minutes=self.__DURATION)
        payload = {
            "sub": username,
            "exp": exp
        }

        return jwt.encode(
            payload=payload,
            key=self.__SECRET,
            algorithm="HS512"
        )

    def verify_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.__SECRET,
                algorithms=["HS512"]
            )

            user = self.__repository.find_user(payload["sub"])
            if user is None:
                return None

            return payload["sub"]

        except jwt.ExpiredSignatureError as e:
            print(str(e))
            return None

        except jwt.InvalidTokenError as e:
            print(str(e))
            return None

        except Exception as e:
            print(str(e))
            return None
