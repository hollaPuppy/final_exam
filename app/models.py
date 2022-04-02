from pydantic import BaseModel


class users(BaseModel):
    fio: str
    hash_pass: str
    img: str
    telegram_name: str
    balance: int
    id_team: int
    telegram_id: str = None
    status: int


class teams(BaseModel):
    coord: str
    team_name: str
    user_cap: str
