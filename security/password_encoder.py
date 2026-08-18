from abc import ABC, abstractmethod


class PasswordEncoder(ABC):
    @abstractmethod
    def encode_password(self, password: str) -> str:
        pass

    @abstractmethod
    def match_password(self, raw_password: str, encrypted_password: str) -> bool:
        pass
