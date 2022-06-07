from typing import Optional

from pydantic import BaseModel


class Achievements_List_Get(BaseModel):
    achv_id: int
    achv_name: str
    achv_req: int
    achv_is_limit: Optional[bool]
    achv_date_end_if_limit: Optional[str]


class Achievements_Limit_List_Get(BaseModel):
    achv_id: int
    achv_name: str
    achv_req: int
    achv_date_end_if_limit: str


class Achievements_Complete_List_Get(BaseModel):
    achv_id: int
    achv_name: str
    user_name: str
    achv_receive_date: str


class Achievements_Process_List_Get(BaseModel):
    user_name: str
    achv_id: int
    achv_name: str
    achv_req: str
    achv_pass: str
    achv_is_limit: Optional[bool]
    achv_date_end_if_limit: Optional[str]


class Achievements_New(BaseModel):
    achv_id: int
    achv_name: str
    achv_req: int
    achv_is_limit: Optional[bool]
    achv_date_end_if_limit: Optional[str]


class Achievements_Process_New(BaseModel):
    achv_id: int
    uid: int
    achv_pass: int


class Achievements_Complete_New(BaseModel):
    achv_id: int
    uid: int
    achv_receive_date: str


class Achievements_Put(BaseModel):
    achv_id: int
    achv_name: str
    achv_req: int
    achv_is_limit: Optional[bool]
    achv_date_end_if_limit: Optional[str]


class Achievements_Process_Put(BaseModel):
    achv_id: int
    uid: int
    achv_pass: int
