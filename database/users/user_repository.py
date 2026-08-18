from src.DTO.user_registration_body import UserRegistrationBody
from src.database.users.schemas import User
from abc import ABC, abstractmethod


class UserRepository(ABC):
    def __init__(self, password_encoder):
        self._password_encoder = password_encoder

    @abstractmethod
    def register(self, user_body: UserRegistrationBody) -> bool:
        pass

    @abstractmethod
    def find_user(self, username: str) -> User | None:
        pass

    @abstractmethod
    def delete(self, username: str) -> bool:
        pass
