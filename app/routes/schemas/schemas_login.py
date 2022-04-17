from pydantic import BaseModel

from app.settings import EMAIL_EXAMPLE


class UserRegSchema(BaseModel):
    username: str
    email: str = EMAIL_EXAMPLE
    password: str


class UserAuthSchema(BaseModel):
    username: str
    password: str
