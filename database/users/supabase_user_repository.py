from src.DTO.user_registration_body import UserRegistrationBody
from src.security.password_encoder import PasswordEncoder
from src.database.users.user_repository import UserRepository
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import create_engine, delete, select
from src.database.users.schemas import User
from dotenv import load_dotenv
from typing_extensions import override
import os


class SupabaseUserRepository(UserRepository):
    def __init__(self, password_encoder: PasswordEncoder):
        super().__init__(password_encoder)
        load_dotenv(
            dotenv_path=".env",
            verbose=False
        )

        self.__engine = create_engine(
            url=os.getenv("SUPABASE_CONNECTION_URL"),
            echo=False
        )
        self.__session = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )

    @override
    def register(self, user_body: UserRegistrationBody) -> bool:
        new_user = User(
            username=user_body.username,
            password=self._password_encoder.encode_password(user_body.password),
            first_name=user_body.first_name.lower(),
            middle_name=user_body.middle_name.lower() if user_body.middle_name is not None else None,
            last_name=user_body.last_name.lower(),
            mobile_number=user_body.mobile_number,
            email_id=user_body.email_id,
            gender=user_body.gender.upper(),
            dob=user_body.dob,
            address=user_body.address.lower()
        )

        with self.__session() as session:
            try:
                session.add(new_user)
                session.commit()
                return True

            except IntegrityError as e:
                print("INTEGRITY ERROR OCCURRED WHILE REGSITERING NEW USER")
                print(str(e))
                session.rollback()
                return False

            except SQLAlchemyError as e:
                print("SOMETHING WENT WRONG WHILE REGISTERING NEW USER")
                print(str(e))
                session.rollback()
                return False

            except Exception as e:
                print("SOMETHING WENT WRONG")
                print(str(e))
                session.rollback()
                return False

    @override
    def find_user(self, username: str) -> User | None:
        statement = select(User).where(
            User.username == username
        ).limit(1)

        with self.__session() as session:
            try:
                user = session.execute(statement).scalars().first()
                return user

            except SQLAlchemyError as e:
                print("SOMETHING WENT WRONG WHILE FETCHING USER FOR LOGIN")
                print(str(e))
                return None

            except Exception as e:
                print("SOMETHING WENT WRONG IN LOGIN")
                print(str(e))
                return None

    @override
    def delete(self, username: str) -> bool:
        statement = delete(User).where(
            User.username == username
        )

        with self.__session() as session:
            try:
                result = session.execute(statement)
                session.commit()
                return result.rowcount == 1

            except SQLAlchemyError as e:
                print("SOMETHING WENT WRONG WHILE DELETING USER ACCOUNT")
                print(str(e))
                session.rollback()
                return False

            except Exception as e:
                print("SOMETHING WENT WRONG")
                print(str(e))
                session.rollback()
                return False
