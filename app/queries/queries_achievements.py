from app.db import DB
from app.routes.schemas.schemas import Achievements_List_Get


async def get_achievements_list() -> list:
    query = f"""
           select name_ach, req_ach
           from achievements_list
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Achievements_List_Get(**row).dict(), result_list))


async def get_limit_achievements_list() -> list:
    query = f"""
           select name_ach, req_ach, date_end_if_limit_ach
           from achievements_list
           where limit_ach = True
           and date_end_if_limit_ach > (select NOW())
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Achievements_List_Get(**row).dict(), result_list))
