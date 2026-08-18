from sqlalchemy import Column, create_engine, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os


class PseudoBase(DeclarativeBase):
    pass


class ChatMetatdata(PseudoBase):

    __tablename__ = "chat_metadata"

    thread_id = Column(
        type_=String(length=500),
        name="thread_id",
        primary_key=True
    )

    username = Column(
        type_=String(length=255),
        name="username",
        index=True,
        nullable=False
    )

    chat_title = Column(
        type_=String(length=500),
        name="chat_title",
        nullable=False
    )

    chat_created = Column(
        type_=DateTime,
        name="chat_created",
        nullable=False
    )


# RUN THIS FILE ONCE TO CREATE THE TABLE
if __name__ == "__main__":
    load_dotenv(
        dotenv_path=".env",
        verbose=False
    )

    SUPABASE_CONNECTION_URL = os.getenv("SUPABASE_CONNECTION_URL")

    try:
        with Session():
            engine = create_engine(url=SUPABASE_CONNECTION_URL)
            PseudoBase.metadata.create_all(bind=engine)

    except SQLAlchemyError as e:
        print(str(e))
        print("COULD NOT CREATE CHAT METADATA TABLE")

    except Exception as e:
        print(str(e))
        print("SOMETHING WENT WRONG WHILE TRYING TO CREATE CHAT METADATA TABLE")
