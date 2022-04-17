from app.db import DB


async def get_achievements_list() -> list:
    query = f"""
           select name_ach, req_ach
           from achievements_list
           where date_end_if_limit_ach < (select NOW())
       """
    result_list = await DB.conn.fetch(query)
    return result_list


async def get_limit_achievements_list() -> list:
    query = f"""
           select name_ach, req_ach
           from achievements_list
           where limit_ach = 1
           and date_end_if_limit_ach < (select NOW())
       """
    result_list = await DB.conn.fetch(query)
    return result_list







