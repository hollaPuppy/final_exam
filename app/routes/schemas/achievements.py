from typing import Optional

from pydantic import BaseModel


class Achievements_List_Get(BaseModel):
    name_ach: str
    req_ach: int


class Achievements_Limit_List_Get(BaseModel):
    name_ach: str
    req_ach: int
    date_end_if_limit_ach: Optional[str]


class Complete_Achievements(BaseModel):
    id_comach: int
    id_ach: int
    uid: int
    date_receive: str


class Process_Achievements(BaseModel):
    id_proach: int
    id_ach: int
    pass_ach: int