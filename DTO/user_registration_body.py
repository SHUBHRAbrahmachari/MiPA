from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional
from datetime import date


class UserRegistrationBody(BaseModel):
    username: str = Field(min_length=8, max_length=255)
    password: str = Field(min_length=8, max_length=255)
    first_name: str = Field(max_length=255)
    middle_name: Optional[str] = Field(default=None, max_length=255)
    last_name: str = Field(max_length=255)
    gender: Literal["MALE", "FEMALE", "OTHER"]
    mobile_number: str = Field(min_length=10, max_length=10)
    email_id: EmailStr
    dob: date
    address: str = Field(max_length=255)
