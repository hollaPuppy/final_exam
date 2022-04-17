from fastapi import APIRouter, Request
from ..utils.user import hash_password, \
                         send_confirm_letter, \
                         check_password_hash
from ..queries.queries_login import check_email_exist, \
                                    check_username_exist, \
                                    registration_user, \
                                    get_pass
from .schemas.schemas_login import UserRegSchema, \
                                   UserAuthSchema
routerUser = APIRouter(
    prefix='/user',
    tags=['user']
)


@routerUser.post("/registration")
async def reg(request: Request, body: UserRegSchema) -> str:
    req: dict = await request.json()
    username = req.get("username")
    email = req.get("email")
    user_pass = req.get("password")

    check_email = await check_email_exist(email)
    if check_email:
        return f"lol email"

    check_username = await check_username_exist(username)
    if check_username:
        return f"mda username"

    hash_pass = hash_password(user_pass)

    answer_code = send_confirm_letter(email)
    if len(answer_code) != 4:
        return f"smth wrong with sending email"

    await registration_user(username, email, hash_pass)
    return answer_code


@routerUser.get("/auth")
async def auth(request: Request, body: UserAuthSchema) -> str:
    req: dict = await request.json()
    username = req.get("username")
    user_pass = req.get("password")

    check_username = await check_username_exist(username)
    if check_username is False:
        return f"mda username"

    db_pass = await get_pass(username)
    if db_pass is None:
        return f"mda password"

    print(check_password_hash(user_pass, db_pass))

    return f"okay"



