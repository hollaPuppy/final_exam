import ujson

from app.db import DB
from datetime import datetime
from app.routes.schemas.saves import Saves_List_By_Username, \
                                     Saves_Complete_Puzs, \
                                     Saves_Coords


async def get_save_record_id(user_name: str, save_name: str) -> str:
    query = f"""
         select save_id 
         from saves 
         where uid = (select uid from users where user_name=$1) 
         and save_name = $2
       """
    return await DB.conn.fetchval(query, user_name, save_name)


async def get_saves_by_username(user_name: str) -> list:
    query = f"""
        select save_name, save_date 
        from saves 
        where uid = (select uid from users where user_name = $1)
        order by save_date
       """
    return list(map(lambda row: Saves_List_By_Username(**row).dict(), await DB.conn.fetch(query, user_name)))


async def get_coords_by_save_id(save_record_id: int) -> list:
    query = f"""
         select coord_pos, coord_rot 
         from coordinations 
         where save_id = $1
       """
    return list(map(lambda row: Saves_Coords(**row).dict(), await DB.conn.fetch(query, save_record_id)))


async def get_complete_puzzles_list(save_record_id: int) -> list:
    query = f"""
         select puz_id
         from complete_puzzles 
         where save_id = $1
       """
    return list(map(lambda row: Saves_Complete_Puzs(**row).dict(), await DB.conn.fetch(query, save_record_id)))


async def post_save_record(user_name: str, save_name: str):
    query = f"""
         insert into saves(uid, save_date, save_name)
         values((select uid from users where user_name = $1), $2, $3) 
       """
    await DB.conn.execute(query, user_name, datetime.now(), save_name)


async def post_coords_records(coord_pos: str, coord_rot: str, save_id: int):
    query = f"""
         insert into coordinations(coord_pos, coord_rot, save_id) 
         values ($1, $2, $3)
       """
    await DB.conn.execute(query, coord_pos, coord_rot, save_id)


async def post_puz_records(puz_id_list: list):
    query = f"""
         insert into complete_puzzles(puz_id, receive_date, save_id) 
         values ($1, $2, $3)
       """
    await DB.conn.executemany(query, puz_id_list)


async def update_coords_records(coord_pos: str, coord_rot: str, save_id: int):
    query = f"""
         update coordinations 
         set coord_pos = $1,
         coord_rot = $2
         where save_id = $3
        """
    await DB.conn.execute(query, coord_pos, coord_rot, save_id)