from src.security.password_encoder import PasswordEncoder
from typing_extensions import override
import bcrypt


class BcryptPasswordEncoder(PasswordEncoder):
    def __init__(self):
        super().__init__()
        self.__SALT = bcrypt.gensalt()

    @override
    def encode_password(self, password: str) -> str:
        password_bytes = password.encode()
        encrypted_password = bcrypt.hashpw(password_bytes, self.__SALT).decode()
        return encrypted_password

    @override
    def match_password(self, raw_password: str, encrypted_password: str) -> bool:
        return bcrypt.checkpw(
            raw_password.encode(),
            encrypted_password.encode()
        )
