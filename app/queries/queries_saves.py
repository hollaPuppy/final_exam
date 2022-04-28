import ujson

from app.db import DB
from datetime import datetime
from app.routes.schemas.saves import Saves_List_By_Username, \
                                     Saves_Complete_Puzs, \
                                     Saves_Coords


async def create_save_record(username: str, save_name: str) -> str:
    query = f"""
         insert into saves(uid, save_date, save_name)
         values((select uid from users where username = $1), $2, $3) 
       """
    try:
        await DB.conn.execute(query, username, datetime.now(), save_name)
    except BaseException as ex:
        return f"Smth wrong! read exception: {ex}"
    finally:
        return f"ok"


async def get_save_record_id(username: str, save_name: str) -> str:
    query = f"""
         select save_id 
         from saves 
         where uid = (select uid from users where username=$1) 
         and save_name = $2
       """
    return await DB.conn.fetchval(query, username, save_name)


async def create_coords_records(coord_pos: str, coord_rot: str, save_id: int) -> None:
    query = f"""
         insert into coordinations(coord_pos, coord_rot, save_id) 
         values ($1, $2, $3)
       """
    return await DB.conn.execute(query, coord_pos, coord_rot, save_id)


async def update_coords_records(coord_pos: str, coord_rot: str, save_id: int) -> None:
    query = f"""
         update coordinations 
         set coord_pos = $1,
         coord_rot = $2
         where save_id = $3
        """
    return await DB.conn.execute(query, coord_pos, coord_rot, save_id)


async def get_saves_by_username(username: str) -> list:
    query = f"""
        select save_name, save_date 
        from saves 
        where uid = (select uid from users where username = $1)
        order by save_date
       """
    result_list = await DB.conn.fetch(query, username)
    return list(map(lambda row: Saves_List_By_Username(**row).dict(), result_list))


async def get_coords_by_save_id(save_record_id: int) -> list:
    query = f"""
         select coord_pos, coord_rot 
         from coordinations 
         where save_id = $1
       """
    result_list = await DB.conn.fetch(query, save_record_id)
    return list(map(lambda row: Saves_Coords(**row).dict(), result_list))


async def create_puz_records(puz_id_list: list) -> None:
    query = f"""
         insert into complete_puzzles(puz_id, receive_date, save_id) 
         values ($1, $2, $3)
       """
    return await DB.conn.executemany(query, puz_id_list)


async def get_complete_puzzles_list(save_record_id: int) -> list:
    query = f"""
         select puz_id
         from complete_puzzles 
         where save_id = $1
       """
    result_list = await DB.conn.fetch(query, save_record_id)
    return list(map(lambda row: Saves_Complete_Puzs(**row).dict(), result_list))



