from pydantic import BaseModel
from typing import Optional


class Lobbies_List(BaseModel):
    lob_id: int
    lob_name: str


class Lobbies_New(BaseModel):
    lob_is_closed: bool
    lob_name: str
    uid: int


class Lobbies_Get_In(BaseModel):
    lob_id: int
    lob_pass_code: Optional[str]
    uid: int


