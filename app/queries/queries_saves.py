import ujson

from app.db import DB
from datetime import datetime


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
    record_id = await DB.conn.fetchval(query, username, save_name)
    return record_id


async def create_puz_records(puz_id_list: list) -> None:
    query = f"""
             insert into complete_puzzles(puz_id, receive_date, save_id) 
             values ($1, $2, $3)
        """
    return await DB.conn.executemany(query, puz_id_list)


async def create_coord_records(coord_pos: str, coord_rot: str, save_id: int) -> None:
    query = f"""
             insert into coordinations(coord_pos, coord_rot, save_id) 
             values ($1, $2, $3)
        """
    return await DB.conn.execute(query, coord_pos, coord_rot,save_id)
