from app.db import DB
from app.routes.schemas.achievements import Achievements_List_Get,\
                                            Achievements_Limit_List_Get, \
                                            Complete_Achievements_List_Get, \
                                            Process_Achievements_List_Get


async def get_achievements_list() -> list:
    query = f"""
         select achv_name, achv_req
         from achievements_list
         order by achv_id
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Achievements_List_Get(**row).dict(), result_list))


async def get_limit_achievements_list() -> list:
    query = f"""
         select achv_name, achv_req, achv_date_end_if_limit
         from achievements_list
         where achv_is_limit = True
         and achv_date_end_if_limit > (select NOW())
         order by achv_name
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Achievements_Limit_List_Get(**row).dict(), result_list))


async def get_complete_achievements_list() -> list:
    query = f"""
         select u.username, al.achv_name, ca.receive_date 
         from complete_achievements ca 
         join users u on u.uid = ca.uid 
         join achievements_list al on al.achv_id = ca.achv_id
         order by ca.receive_date
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Complete_Achievements_List_Get(**row).dict(), result_list))


async def get_complete_achievements_by_username(username: str) -> list:
    query = f"""
         select al.achv_name, ca.receive_date 
         from complete_achievements ca 
         join users u on u.uid = ca.uid 
         join achievements_list al on al.achv_id = ca.achv_id
         where u.username=$1
         order by ca.receive_date 
       """
    result_list = await DB.conn.fetch(query, username)
    return list(map(lambda row: Complete_Achievements_List_Get(**row).dict(), result_list))


async def get_process_achievements_list() -> list:
    query = f"""
         select al.achv_name, al.achv_req, pa.achv_pass, al.achv_date_end_if_limit
         from process_achievements pa 
         join achievements_list al on al.achv_id = pa.achv_id
         order by al.achv_date_end_if_limit
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Process_Achievements_List_Get(**row).dict(), result_list))


async def get_process_achievements_by_username(username: str) -> list:
    query = f"""
         select al.achv_name, al.achv_req, pa.achv_pass, al.achv_date_end_if_limit 
         from process_achievements pa 
         join users u on u.uid = pa.uid
         join achievements_list al on al.achv_id = pa.achv_id
         where u.username=$1
         order by al.achv_date_end_if_limit
       """
    result_list = await DB.conn.fetch(query, username)
    return list(map(lambda row: Process_Achievements_List_Get(**row).dict(), result_list))

# __________POST_________________


async def post_achievement(request: dict) -> None:
    req: dict = await request.json()
    achv_name = req.get("achv_name")
    achv_req = req.get("achv_req")
    achv_is_limit = req.get("achv_is_limit")
    achv_date_end_if_limit = req.get("achv_date_end_if_limit")
    query = f"""
         insert into achievements_list(achv_name, achv_req, achv_is_limit, achv_date_end_if_limit)
         values ($1, $2, $3, $4)
       """
    await DB.conn.execute(query, achv_name, achv_req, achv_is_limit, achv_date_end_if_limit)
    return f"ok"
