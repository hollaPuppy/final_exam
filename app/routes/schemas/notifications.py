from pydantic import BaseModel
from typing import Optional


class Notifications_List(BaseModel):
    ntfct_title: str
    ntfct_text: str
    ntfct_date: str
    ntfct_opened: bool


class Notifications_Post_New(BaseModel):
    ntfct_title: str
    ntfct_text: str
    ntfct_date: Optional[str]


class Notifications_Put_Opened(BaseModel):
    ntfct_id: int
    username: str
