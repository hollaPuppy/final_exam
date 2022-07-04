from pydantic import BaseModel
from typing import Optional

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


class User_Info(BaseModel):
    user_name: str
    user_email: str = EMAIL_EXAMPLE
    user_active_time: str


class User_List_By_Active_Time(BaseModel):
    user_name: str
    user_active_time: Optional[str]


class User_Active_Time_Put(BaseModel):
    uid: int
    user_active_time: str


class User_Info_Put(BaseModel):
    user_name: Optional[str]
    user_email: Optional[str] = EMAIL_EXAMPLE
