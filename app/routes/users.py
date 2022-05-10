from fastapi import APIRouter, \
                    Request, \
                    HTTPException
from fastapi.responses import UJSONResponse
from ..utils.users import hash_password, \
                          send_confirm_letter, \
                          check_password_hash
from ..queries.queries_users import get_check_email_exist, \
                                    get_check_username_exist, \
                                    get_pass, \
                                    get_uid_by_username, \
                                    post_registration_user
from .schemas.users import User_Reg, \
                           User_Auth
routerUser = APIRouter(
    prefix='/users',
    tags=['users']
)


@routerUser.post("/registration")
async def reg(request: Request, body: User_Reg) -> str:
    req: dict = await request.json()
    user_name = req.get("user_name")
    user_email = req.get("user_email")
    user_password = req.get("user_password")

    if await get_check_email_exist(user_email):
        raise HTTPException(status_code=409, detail=f"Email already exists")

    if await get_check_username_exist(user_name):
        raise HTTPException(status_code=409, detail=f"User already exists")
    hash_pass = await hash_password(user_password)

    answer_code = await send_confirm_letter(user_email)
    if len(answer_code) != 4:
        raise HTTPException(status_code=500, detail=f"Bad email sending")

    if await post_registration_user(user_name, user_email, hash_pass) is not None:
        raise HTTPException(status_code=500, detail=f"User has not been registered")

    uid = get_uid_by_username(user_name)

    return UJSONResponse({'code': answer_code, 'uid': uid})


@routerUser.get("/auth")
async def auth(request: Request, body: User_Auth) -> str:
    req: dict = await request.json()
    user_name = req.get("username")
    user_password = req.get("password")

    if not await get_check_username_exist(user_name):
        raise HTTPException(status_code=404, detail=f"User {username} not found")

    db_pass = await get_pass(user_name)

    if not await check_password_hash(user_password, db_pass):
        raise HTTPException(status_code=409, detail=f"Wrong password")

    return HTTPException(status_code=200, detail=f"OK")



