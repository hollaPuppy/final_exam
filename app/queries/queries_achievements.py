from app.db import DB
from typing import Optional
from app.routes.schemas.achievements import Achievements_List_Get,\
                                            Achievements_Limit_List_Get, \
                                            Achievements_Complete_List_Get, \
                                            Achievements_Process_List_Get


async def get_achievements_list() -> list:
    query = f"""
         select achv_id, achv_name, achv_req, achv_is_limit, achv_date_end_if_limit
         from achievements_list
         order by achv_id
       """
    return list(map(lambda row: Achievements_List_Get(**row).dict(), await DB.conn.fetch(query)))


async def get_check_achievement(achv_id: int) -> list:
    query = f"""
         select exists (
         select
         from achievements_list
         where achv_id = $1)
       """
    return await DB.conn.fetchval(query, achv_id)


async def get_achievement_id(achv_name: str, achv_req: int) -> int:
    query = f"""
         select achv_id
         from achievements_list
         where achv_name = $1
         and achv_req = $2
       """
    return await DB.conn.fetchval(query, achv_name, achv_req)


async def get_limit_achievements_list() -> list:
    query = f"""
         select achv_id, achv_name, achv_req, achv_date_end_if_limit
         from achievements_list
         where achv_is_limit = True
         and achv_date_end_if_limit > (select NOW())
         order by achv_name
       """
    return list(map(lambda row: Achievements_Limit_List_Get(**row).dict(), await DB.conn.fetch(query)))


async def get_complete_achievements_list() -> list:
    query = f"""
         select al.achv_id, al.achv_name, u.username, ca.achv_receive_date 
         from complete_achievements ca 
         join users u on u.uid = ca.uid 
         join achievements_list al on al.achv_id = ca.achv_id
         order by ca.achv_receive_date
       """
    return list(map(lambda row: Achievements_Complete_List_Get(**row).dict(), await DB.conn.fetch(query)))


async def get_complete_achievements_by_username(username: str) -> list:
    query = f"""
         select al.achv_id, al.achv_name, u.username, ca.achv_receive_date
         from complete_achievements ca 
         join users u on u.uid = ca.uid 
         join achievements_list al on al.achv_id = ca.achv_id
         where u.username=$1
         order by ca.achv_receive_date 
       """
    return list(map(lambda row: Achievements_Complete_List_Get(**row).dict(), await DB.conn.fetch(query, username)))


async def get_process_achievements_list() -> list:
    query = f"""
         select al.achv_id, al.achv_name, al.achv_req, pa.achv_pass, al.achv_date_end_if_limit
         from process_achievements pa 
         join achievements_list al on al.achv_id = pa.achv_id
         order by al.achv_date_end_if_limit
       """
    return list(map(lambda row: Achievements_Process_List_Get(**row).dict(), await DB.conn.fetch(query)))


async def get_process_achievements_by_username(username: str) -> list:
    query = f"""
         select al.achv_id, al.achv_name, al.achv_req, pa.achv_pass, al.achv_date_end_if_limit 
         from process_achievements pa 
         join users u on u.uid = pa.uid
         join achievements_list al on al.achv_id = pa.achv_id
         where u.username=$1
         order by al.achv_date_end_if_limit
       """
    return list(map(lambda row: Achievements_Process_List_Get(**row).dict(), await DB.conn.fetch(query, username)))

# __________POST_________________


async def post_achievement(achv_name: str,
                           achv_req: int,
                           achv_is_limit: Optional[bool],
                           achv_date_end_if_limit: Optional[str]) -> bool:
    query = f"""
         insert into achievements_list(achv_name, achv_req, achv_is_limit, achv_date_end_if_limit)
         values ($1, $2, $3, $4)
       """
    await DB.conn.execute(query,
                          achv_name,
                          achv_req,
                          achv_is_limit,
                          achv_date_end_if_limit)
    return True


async def post_process_achievement(achv_id: int, uid: int, achv_pass: int) -> bool:
    query = f"""
         insert into process_achievements(achv_id, uid, achv_pass)
         values ($1, $2, $3)
       """
    await DB.conn.execute(query, achv_id, uid, achv_pass)
    return True


async def post_complete_achievement(achv_id: int, uid: int, achv_receive_date: str) -> bool:
    query = f"""
         insert into complete_achievements(achv_id, uid, achv_receive_date)
         values ($1, $2, $3)
       """
    await DB.conn.execute(query, achv_id, uid, achv_receive_date)
    return True


# __________Put_________________


async def put_achievement(achv_id: int,
                          achv_name: str,
                          achv_req: int,
                          achv_is_limit: Optional[bool],
                          achv_date_end_if_limit: Optional[str]) -> bool:
    query = f"""
         update achievements_list 
         set achv_name = $1, 
         achv_req = $2, 
         achv_is_limit = $3, 
         achv_date_end_if_limit = $4
         where achv_id = $5
       """
    await DB.conn.execute(query,
                          achv_name,
                          achv_req,
                          achv_is_limit,
                          achv_date_end_if_limit,
                          achv_id)
    return True


async def put_process_achievement(achv_id: int,
                                  uid: str,
                                  achv_pass: int) -> bool:
    query = f"""
         update process_achievements
         set achv_pass = $1
         where achv_id = $2
         and uid = $3
       """
    await DB.conn.execute(query,
                          achv_pass,
                          achv_id,
                          uid)
    return True
