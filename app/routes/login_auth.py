import os
import hashlib
import jwt
from fastapi import APIRouter, Request, Response
from app.db import DB
from ..settings import SECRET_KEY

routerUser = APIRouter(
    prefix='/user',
    tags=['user']
)


@routerUser.post("/registration")
async def reg(request: Request) -> str:
    req: dict = await request.json()
    username = req.get("username")
    email = req.get("email")
    user_pass = req.get("password")
    query_check_email = f"""
                     select exists (
                            select
                            from users
                            where email = $1)
    """
    check = await DB.conn.fetchval(query_check_email, email)
    if check:
        return "lol"

    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', user_pass.encode('utf-8'), salt, 100000)
    hash_pass = (salt + key).hex()

    query_reg_user = f"""
         insert into users(username, email, hash_pass)
         values($1, $2, $3)
    """

    await DB.conn.execute(query_reg_user, username, email, hash_pass)
    return "all well"
