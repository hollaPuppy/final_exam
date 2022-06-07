import ujson
from app.db import DB
from datetime import datetime
from app.routes.schemas.users import User_Uid_List, \
                                     User_Info


async def get_check_email_exist(email: str) -> bool:
    query = f"""
         select exists (
         select
         from users
         where user_email = $1)
       """
    return await DB.conn.fetchval(query, email)


async def get_check_uid_exist(uid: int) -> bool:
    query = f"""
         select exists (
         select
         from users
         where uid = $1)
       """
    return await DB.conn.fetchval(query, uid)


async def get_pass(username: str) -> str:
    query = f"""
         select user_hash_pass
         from users
         where user_name = $1s
       """
    return await DB.conn.fetchval(query, username)


async def get_check_username_exist(username: str) -> bool:
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


async def get_check_user_by_uid(uid: int) -> bool:
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


async def get_username_by_uid(uid: int) -> str:
    query = f"""
         select user_name
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
    # сделать парсилку времени к часам - 1;12;0 - часов;минут;секунд в игре

    # убрать лямбду, тут не нужен такой цикл, убрать везде в подобных
    return list(map(lambda row: User_Info(**row).dict(), await DB.conn.fetchval(query, uid)))


async def post_registration_user(username: str, email: str, hash_pass: dict) -> None:
    query = f"""
         insert into users(user_name, user_email, user_hash_pass)
         values($1, $2, $3)
       """
    await DB.conn.execute(query, username, email, ujson.dumps(hash_pass))




