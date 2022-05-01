from app.db import DB

from app.routes.schemas.lobbies import Lobbies_List


async def get_lobbies_list() -> list:
    query = f"""
         select lob_id, lob_name
         from lobbies
         where lob_is_closed = 0
         and lob_is_full = 0
         order by lob_create_date
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: Lobbies_List(**row).dict(), result_list))


async def get_created_lobby(lob_name: str, lob_create_date: str) -> list:
    query = f"""
         select lob_id
         from lobbies
         where lob_name = $1
         and lob_create_date = $2
       """
    result_id = await DB.conn.fetchval(query, lob_name, lob_create_date)
    return result_id

# __________POST_________________


async def post_lobby(lob_is_closed: bool,
                     lob_pass_code: str,
                     lob_name: str,
                     lob_create_date: str) -> str:
    query = f"""
             insert into lobbies(lob_is_closed, lob_pass_code, lob_name, lob_create_date, lob_is_full)
             values ($1, $2, $3, $4, 0)
           """
    await DB.conn.execute(query, lob_is_closed, lob_pass_code, lob_name, lob_create_date)
    return f"ok"


async def post_cap_lobby(uid: int, lob_id: int) -> str:
    query = f"""
         insert into lobbies_users(uid, lob_is_cap, lob_id)
         values ($1, 1, $2)
       """
    await DB.conn.execute(query, uid, lob_id)
    return f"ok"


async def get_lob_openness(lob_name: str, lob_create_date: str) -> list:
    query = f"""
         select lob_is_clos
         from lobbies
         where lob_name = $1
         and lob_create_date = $2
       """
    result_id = await DB.conn.fetchval(query, lob_name, lob_create_date)
    return result_id

