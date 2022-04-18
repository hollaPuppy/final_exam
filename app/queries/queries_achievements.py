from app.db import DB
from app.routes.schemas.achievements import Achievements_List_Get,\
                                            Achievements_Limit_List_Get, \
                                            Complete_Achievements_List_Get, \
                                            Process_Achievements_List_Get


async def get_achievements_list() -> list:
    query = f"""
           select name_ach, req_ach
           from achievements_list
           order by id_ach
        """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Achievements_List_Get(**row).dict(), result_list))


async def get_limit_achievements_list() -> list:
    query = f"""
           select name_ach, req_ach, date_end_if_limit_ach
           from achievements_list
           where limit_ach = True
           and date_end_if_limit_ach > (select NOW())
           order by name_ach
        """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Achievements_Limit_List_Get(**row).dict(), result_list))


async def get_complete_achievements_list() -> list:
    query = f"""select al.name_ach, u.username, ca.date_receive 
            from complete_achievements ca 
            join users u on u.uid = ca.uid 
            join achievements_list al on al.id_ach = ca.id_ach
            order by ca.date_receive
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Complete_Achievements_List_Get(**row).dict(), result_list))


async def get_complete_achievements_by_username(username: str) -> list:
    query = f"""select al.name_ach, u.username, ca.date_receive 
            from complete_achievements ca 
            join users u on u.uid = ca.uid 
            join achievements_list al on al.id_ach = ca.id_ach
            where u.username=$1
            order by ca.date_receive 
       """
    result_list = await DB.conn.fetch(query, username)
    return list(map(lambda row: Complete_Achievements_List_Get(**row).dict(), result_list))


async def get_process_achievements_list() -> list:
    query = f"""select al.name_ach, u.username, al.req_ach, pa.pass_ach, al.date_end_if_limit_ach as date_limit 
            from process_achievements pa 
            join users u on u.uid = pa.uid 
            join achievements_list al on al.id_ach = pa.id_ach
            order by al.date_end_if_limit_ach
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Process_Achievements_List_Get(**row).dict(), result_list))


async def get_process_achievements_by_username(username: str) -> list:
    query = f"""select al.name_ach, u.username, al.req_ach, pa.pass_ach, al.date_end_if_limit_ach as date_limit 
            from process_achievements pa 
            join users u on u.uid = pa.uid 
            join achievements_list al on al.id_ach = pa.id_ach
            where u.username=$1
            order by al.date_end_if_limit_ach
       """
    result_list = await DB.conn.fetch(query, username)
    return list(map(lambda row: Process_Achievements_List_Get(**row).dict(), result_list))

