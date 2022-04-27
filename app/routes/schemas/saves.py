from typing import Optional

from pydantic import BaseModel


class Saves_Set_New(BaseModel):
    username: str
    save_name: str
    coord_pos: str
    coord_rot: str
    puz_id_list: str


class Saves_List_By_Username(BaseModel):
    save_name: str
    save_date: str


class Saves_Full_Info(BaseModel):
    username: str
    save_name: str


class Saves_Coords(BaseModel):
    coord_pos: str
    coord_rot: str


class Saves_Complete_Puzs(BaseModel):
    puz_id: int



