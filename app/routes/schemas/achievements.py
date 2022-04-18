from typing import Optional

from pydantic import BaseModel


class Achievements_List_Get(BaseModel):
    name_ach: str
    req_ach: int


class Achievements_Limit_List_Get(BaseModel):
    name_ach: str
    req_ach: int
    date_end_if_limit_ach: str


class Complete_Achievements_List_Get(BaseModel):
    name_ach: str
    username: str
    date_receive: str


class Process_Achievements_List_Get(BaseModel):
    name_ach: str
    username: str
    req_ach: str
    pass_ach: str
    date_limit: Optional[str]