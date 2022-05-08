import ujson
from app.db import DB
from datetime import datetime
from app.routes.schemas.users import User_Uid_List


async def get_check_email_exist(email: str) -> str:
    query = f"""
         select exists (
         select
         from users
         where user_email = $1)
       """
    return await DB.conn.fetchval(query, email)


async def get_pass(username: str) -> str:
    query = f"""
         select user_hash_pass
         from users
         where user_name = $1s
       """
    return await DB.conn.fetchval(query, username)


async def get_check_username_exist(username: str) -> str:
    query = f"""
         select exists (
         select
         from users
         where user_name = $1)
       """
    return await DB.conn.fetchval(query, username)


async def get_uid_list() -> list:
    query = f"""
         select uid
         from users
       """
    result_list = await DB.conn.fetch(query)
    return list(map(lambda row: User_Uid_List(**row).dict(), result_list))


async def get_check_user_by_uid(uid: int) -> list:
    query = f"""
         select exists (
         select
         from users
         where uid = $1)
       """
    return await DB.conn.fetchval(query, uid)


async def get_uid_by_username(username: str) -> list:
    query = f"""
         select uid
         from users
         where user_name = $1
       """
    return await DB.conn.fetchval(query, username)


async def post_registration_user(username: str, email: str, hash_pass: dict) -> bool:
    query = f"""
         insert into users(user_name, user_email, user_hash_pass)
         values($1, $2, $3)
       """
    await DB.conn.execute(query, username, email, ujson.dumps(hash_pass))




