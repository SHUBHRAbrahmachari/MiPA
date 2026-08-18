from pydantic import BaseModel, Field


class UserLoginBody(BaseModel):
    username: str = Field(min_length=8, max_length=255)
    password: str = Field(min_length=8, max_length=255)
