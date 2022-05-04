from pydantic import BaseModel

from app.settings import EMAIL_EXAMPLE


class User_Reg(BaseModel):
    username: str
    email: str = EMAIL_EXAMPLE
    password: str


class User_Auth(BaseModel):
    username: str
    password: str


class User_Uid_List(BaseModel):
    uid: int

