from app.db import DB


async def get_achievements_list() -> str:
    query = f"""
           select name_ach, req_ach
           from achievements_list
           where date_end_if_limit_ach < (select NOW())
       """
    return await DB.conn.fetchval(query)
