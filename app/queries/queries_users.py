import ujson
from app.db import DB
from datetime import datetime
from app.routes.schemas.users import User_Uid_List, \
                                     User_Info, \
                                     User_List_By_Active_Time
from ..utils.users import parse_active_time
import json


async def get_email_check_exist(email: str) -> bool:
    query = f"""
         select exists (
         select
         from users
         where user_email = $1)
       """
    return await DB.conn.fetchval(query, email)


async def get_uid_check_exist(uid: int) -> bool:
    query = f"""
         select exists (
         select
         from users
         where uid = $1)
       """
    return await DB.conn.fetchval(query, uid)


async def get_user_password(username: str) -> str:
    query = f"""
         select user_hash_pass
         from users
         where user_name = $1s
       """
    return await DB.conn.fetchval(query, username)


async def get_user_name_check_exist(username: str) -> bool:
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
    return list(map(lambda row: User_Uid_List(**row).dict(), await DB.conn.fetch(query)))


async def get_user_by_uid_check(uid: int) -> bool:
    query = f"""
         select exists (
         select
         from users
         where uid = $1)
       """
    return await DB.conn.fetchval(query, uid)


async def get_uid_by_username(username: str) -> str:
    query = f"""
         select uid
         from users
         where user_name = $1
       """
    return await DB.conn.fetchval(query, username)


async def get_user_name_by_uid(uid: int) -> str:
    query = f"""
         select user_name
         from users
         where uid = $1
       """
    return await DB.conn.fetchval(query, uid)


async def get_user_email_by_uid(uid: int) -> str:
    query = f"""
         select user_email
         from users
         where uid = $1
       """
    return await DB.conn.fetchval(query, uid)


async def get_user_info_by_uid(uid: int) -> list:
    query = f"""
         select user_name, user_email, user_active_time
         from users
         where uid = $1
       """
    raw_info = dict(await DB.conn.fetchrow(query, uid))
    return await parse_active_time(raw_info)


async def get_user_list_by_active_time() -> list:
    query = f"""
         select user_name, user_active_time 
         from users 
         order by user_active_time
       """
    return list(map(lambda row: User_List_By_Active_Time(**row).dict(), await DB.conn.fetch(query)))


async def post_user_registration(username: str, email: str, hash_pass: dict) -> None:
    query = f"""
         insert into users(user_name, user_email, user_hash_pass)
         values($1, $2, $3)
       """
    await DB.conn.execute(query, username, email, ujson.dumps(hash_pass))


async def put_user_active_time(uid: int, user_active_time: str) -> None:
    query = f"""
         update users set user_active_time = $2
         where uid = $1
       """
    await DB.conn.execute(query, uid, user_active_time)


async def put_user_info(uid: int, user_name: str, user_email: str) -> None:
    query = f"""
         update users set user_name = $2,
         user_email = $3
         where uid = $1
       """
    await DB.conn.execute(query, uid, user_name, user_email)

