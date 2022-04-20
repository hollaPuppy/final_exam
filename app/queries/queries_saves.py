import ujson

from app.db import DB
from datetime import datetime


async def create_save_record(username: str, save_name: str) -> str:
    query = f"""
         insert into saves(uid, save_date, save_name)
         values((select uid from users where username = $1), $2, $3) 
    """
    a = await DB.conn.execute(query, username, datetime.now(), save_name)
    print(a)

    return a
