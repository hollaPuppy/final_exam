import ujson

from app.db import DB
from datetime import datetime


async def check_email_exist(email: str) -> str:
    query = f"""
         select exists (
         select
         from users
         where email = $1)
       """
    return await DB.conn.fetchval(query, email)


async def check_username_exist(username: str) -> str:
    query = f"""
         select exists (
         select
         from users
         where username = $1)
       """
    return await DB.conn.fetchval(query, username)


async def registration_user(username: str, email: str, hash_pass: dict) -> None:
    query = f"""
         insert into users(username, email, hash_pass)
         values($1, $2, $3)
       """
    await DB.conn.execute(query, username, email, ujson.dumps(hash_pass))


async def get_pass(username: str) -> str:
    query = f"""
         select hash_pass
         from users
         where username = $1
       """
    return await DB.conn.fetchval(query, username)

