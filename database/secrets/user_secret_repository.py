from abc import abstractmethod, ABC


class UserSecretsRepository(ABC):
    @abstractmethod
    def add_or_update_key(self, username: str, key_name: str, key: str) -> bool:
        pass

    @abstractmethod
    def find_key(self, username: str, key_name: str) -> str | None:
        pass
