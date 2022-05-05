from pydantic import BaseModel

from app.settings import EMAIL_EXAMPLE


class User_Reg(BaseModel):
    user_name: str
    user_email: str = EMAIL_EXAMPLE
    user_password: str


class User_Auth(BaseModel):
    user_name: str
    user_password: str


class User_Uid_List(BaseModel):
    uid: int

