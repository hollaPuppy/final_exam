from pydantic import BaseModel


class users(BaseModel):
    uid: int
    first_name: str
    second_name: str
    last_name: str
    email: str
    hash_pass: str


class achievements_list(BaseModel):
    id_ach: int
    name_ach: str
    req_ach: int
    limit_ach: bool
    date_end_if_limit_ach: str


class complete_achievements(BaseModel):
    id_comach: int
    id_ach: int
    uid: int
    date_receive: str


class process_achievements(BaseModel):
    id_proach: int
    id_ach: int
    pass_ach: int


class messages(BaseModel):
    id_mes: int
    uid_sender: int
    uid_recipient: int
    text_mes: str
    time_mes: str


class saves(BaseModel):
    id_save: int
    uid: int
    date_save: str
    name_save: str


class coordinators(BaseModel):
    id_coord: int
    value_coord: str
    id_save: int


class bd_options(BaseModel):
    id_option: int
    name_option: str
    value_option: str





