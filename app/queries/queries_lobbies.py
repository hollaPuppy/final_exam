from app.db import DB

from app.routes.schemas.lobbies import Lobbies_List


async def get_lob_list() -> list:
    query = f"""
         select lob_id, lob_name
         from lobbies
         where lob_is_closed = 0
         and lob_is_full = 0
         order by lob_create_date
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Lobbies_List(**row).dict(), result_list))


async def get_lob_id(lob_name: str, lob_create_date: str) -> int:
    query = f"""
         select lob_id
         from lobbies
         where lob_name = $1
         and lob_create_date = $2
       """
    return await DB.conn.fetchval(query, lob_name, lob_create_date)


async def get_lob_fullness(lob_id: int) -> int:
    query = f"""
         select lob_is_full
         from lobbies
         where lob_id = $1
       """
    return await DB.conn.fetchval(query, lob_id)


async def get_lob_pass(lob_id: int) -> int:
    query = f"""
         select lob_pass_code
         from lobbies
         where lob_id = $1
       """
    return await DB.conn.fetchval(query, lob_id)


async def get_lob_usr_is_cap(uid: int, lob_id: int) -> int:
    query = f"""
         select lob_is_cap
         from lobbies_users
         where uid = $1
         and lob_id = $2
       """
    return await DB.conn.fetchval(query, uid, lob_id)


async def get_lob_usr_count(lob_id: int) -> int:
    query = f"""
         select count(uid)
         from lobbies_users
         and lob_id = $1
       """
    return await DB.conn.fetchval(query, uid)


async def get_lob_usr_id(lob_id: int, lob_is_cap: bool) -> int:
    query = f"""
         select uid
         from lobbies_users
         and lob_id = $1
         and lob_is_cap = $2
       """
    return await DB.conn.fetchval(query, lob_id, lob_is_cap)


async def post_lob(lob_is_closed: bool,
                   lob_pass_code: str,
                   lob_name: str,
                   lob_create_date: str):
    query = f"""
         insert into lobbies(lob_is_closed, lob_pass_code, lob_name, lob_create_date, lob_is_full)
         values ($1, $2, $3, $4, false)
       """
    await DB.conn.execute(query, lob_is_closed, lob_pass_code, lob_name, lob_create_date)


async def post_lob_usr(uid: int, lob_is_cap: bool, lob_id: int):
    query = f"""
         insert into lobbies_users(uid, lob_is_cap, lob_id)
         values ($1, $2, $3)
       """
    await DB.conn.execute(query, uid, lob_is_cap, lob_id)


async def put_lob_fullness(lob_id: int) -> str:
    query = f"""
         update lobbies set lob_is_full = true
         where lob_id = $1
       """
    await DB.conn.execute(query, lob_id)


async def put_lob_usr_role(uid: int, lob_is_cap: bool, lob_id: int):
    query = f"""
         update lobbies_users set lob_is_cap = $1
         where uid = $2
         and lob_id = $3
       """
    await DB.conn.execute(query, lob_is_cap, uid, lob_id)


async def delete_lob_usr(uid: int, lob_id: int):
    query = f"""
         delete from lobbies_users 
         where uid = $1
         and lob_id = $2 
       """
    await DB.conn.execute(query, uid, lob_id)


async def delete_lob(lob_id: int):
    query = f"""
         delete from lobbies 
         and lob_id = $1 
       """
    await DB.conn.execute(query, lob_id)
