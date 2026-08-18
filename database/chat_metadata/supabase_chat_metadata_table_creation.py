from src.database.chat_metadata.chat_metadata_schema import PseudoBase
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

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
            print("TABLE CHAT METADATA CREATED SUCCESSFULLY")

    except SQLAlchemyError as e:
        print(str(e))
        print("COULD NOT CREATE CHAT METADATA TABLE")

    except Exception as e:
        print(str(e))
        print("SOMETHING WENT WRONG WHILE TRYING TO CREATE CHAT METADATA TABLE")
