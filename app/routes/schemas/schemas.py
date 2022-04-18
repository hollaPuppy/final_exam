# from typing import Optional
#
# from pydantic import BaseModel
#
#
# class Users(BaseModel):
#     uid: int
#     first_name: str
#     second_name: str
#     last_name: str
#     email: str
#     hash_pass: str
#
#
# class Achievements_List(BaseModel):
#     id_ach: int
#     name_ach: str
#     req_ach: int
#     limit_ach: bool
#     date_end_if_limit_ach: str
#
#
# class Achievements_List_Get(BaseModel):
#     name_ach: str
#     req_ach: int
#
#
# class Achievements_Limit_List_Get(BaseModel):
#     name_ach: str
#     req_ach: int
#     date_end_if_limit_ach:Optional[str]
#
#
# class Complete_Achievements(BaseModel):
#     id_comach: int
#     id_ach: int
#     uid: int
#     date_receive: str
#
#
# class Process_Achievements(BaseModel):
#     id_proach: int
#     id_ach: int
#     pass_ach: int
#
#
# class Messages(BaseModel):
#     id_mes: int
#     uid_sender: int
#     uid_recipient: int
#     text_mes: str
#     time_mes: str
#
#
# class Saves(BaseModel):
#     id_save: int
#     uid: int
#     date_save: str
#     name_save: str
#
#
# class Coordinators(BaseModel):
#     id_coord: int
#     value_coord: str
#     id_save: int
#
#
# class Bd_Options(BaseModel):
#     id_option: int
#     name_option: str
#     value_option: str
