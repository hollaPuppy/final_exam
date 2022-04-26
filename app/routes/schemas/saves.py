from typing import Optional

from pydantic import BaseModel


class Saves_Set_New(BaseModel):
    username: str
    save_name: str
    coord_pos: str
    coord_rot: str
    puz_id_list: str



