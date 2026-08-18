from sqlalchemy.schema import Column
from sqlalchemy import String, Date, Enum, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv(
    dotenv_path=".env",
    verbose=False
)

CONNECTION_STRING = os.getenv("SUPABASE_CONNECTION_URL")


class PseudoBase(DeclarativeBase):
    pass


class User(PseudoBase):
    __tablename__ = "users"

    username = Column(
        type_=String(length=255),
        primary_key=True,
        name="username"
    )

    password = Column(
        type_=String(length=255),
        nullable=False,
        name="password"
    )

    first_name = Column(
        type_=String(length=255),
        nullable=False,
        name="first_name"
    )

    middle_name = Column(
        type_=String(length=255),
        nullable=True,
        name="middle_name"
    )

    last_name = Column(
        type_=String(length=255),
        nullable=False,
        name="last_name"
    )

    mobile_number = Column(
        type_=String(length=10),
        nullable=False,
        name="mobile_number",
        unique=True
    )

    email_id = Column(
        type_=String(length=255),
        nullable=False,
        name="email_id",
        unique=True
    )

    gender = Column(
        type_=Enum("MALE", "FEMALE", "OTHER", name="gender_enum"),
        nullable=False,
        name="gender"
    )

    dob = Column(
        type_=Date,
        nullable=False,
        name="dob"
    )

    address = Column(
        type_=String(length=255),
        nullable=False,
        name="address"
    )


if __name__ == "__main__":
    try:
        with Session():
            engine = create_engine(url=CONNECTION_STRING)

            PseudoBase.metadata.create_all(
                bind=engine
            )

    except SQLAlchemyError as e:
        print(str(e))

    except Exception as e:
        print(str(e))
