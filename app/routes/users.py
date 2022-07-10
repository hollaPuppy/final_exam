from cgi import test
from fastapi import APIRouter, \
                    Request, \
                    HTTPException
from fastapi.responses import UJSONResponse
from ..utils.users import hash_password, \
                          send_confirm_letter, \
                          check_password_hash
from ..queries.queries_users import get_uid_check_exist, \
                                    get_user_info_by_uid, \
                                    get_user_email_by_uid, \
                                    get_user_name_by_uid, \
                                    get_email_check_exist, \
                                    get_user_name_check_exist, \
                                    get_user_password, \
                                    get_uid_by_user_name, \
                                    get_user_list_by_active_time, \
                                    post_user_registration, \
                                    put_user_active_time, \
                                    put_user_info
from .schemas.users import User_Reg, \
                           User_Auth, \
                           User_Active_Time_Put, \
                           User_Info_Put
from tasks.tasks_ursers import test_task

routerUser = APIRouter(
    prefix='/users',
    tags=['users']
)


@routerUser.post("/registration")
async def reg(request: Request, body: User_Reg) -> UJSONResponse:
    req: dict = await request.json()
    user_name = req.get("user_name")
    user_email = req.get("user_email")
    user_password = req.get("user_password")

    if await get_email_check_exist(user_email):
        raise HTTPException(status_code=409, detail=f"Email already exists")

    if await get_user_name_check_exist(user_name):
        raise HTTPException(status_code=409, detail=f"User already exists")
    hash_pass = await hash_password(user_password)

    if len(user_password) < 8:
        raise HTTPException(status_code=409, detail=f"Password is too short")

    # answer_code_or_ex = await send_confirm_letter(user_email)
    # if len(answer_code_or_ex) != 4:
    #     raise HTTPException(status_code=500, detail=f"Bad email sending with {answer_code_or_ex}")
    # больше не работает...............
    if await post_user_registration(user_name, user_email, hash_pass) is not None:
        raise HTTPException(status_code=500, detail=f"User has not been registered")

    uid = await get_uid_by_user_name(user_name)

    return UJSONResponse({'uid': uid})


@routerUser.get("/auth")
async def auth(request: Request, body: User_Auth) -> HTTPException:
    req: dict = await request.json()
    user_name = req.get("user_name")
    user_password = req.get("user_password")
    test_task.delay()

    if not await get_user_name_check_exist(user_name):
        raise HTTPException(status_code=404, detail=f"User {user_name} not found")

    db_pass = await get_user_password(user_name)

    if not await check_password_hash(user_password, db_pass):
        raise HTTPException(status_code=409, detail=f"Wrong password")

    return HTTPException(status_code=200, detail=f"OK")


@routerUser.get("/profile/{uid}")
async def profile(uid: int) -> UJSONResponse:
    if not await get_uid_check_exist(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    user_info = await get_user_info_by_uid(uid)

    return UJSONResponse({'profile': user_info})


@routerUser.get("/top_players/{category}")
async def top(category: str) -> UJSONResponse:
    if category == "achv":
        return UJSONResponse({'info': 'cool'})
    if category == "active_time":
        return UJSONResponse({'info': await get_user_list_by_active_time()})
    else:
        return UJSONResponse({'info': 'taheck category'})


@routerUser.put("/put_active_time")
async def put_time(request: Request, body: User_Active_Time_Put) -> HTTPException:
    req: dict = await request.json()
    uid = req.get("uid")
    user_active_time = req.get("user_active_time")
    if not await get_uid_check_exist(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    if await put_user_active_time(uid, user_active_time):
        raise HTTPException(status_code=500, detail=f"Active time dont set")

    raise HTTPException(status_code=200, detail=f"OK")


@routerUser.put("/put/profile/{uid}")
async def put_profile(request: Request, uid: int, body: User_Info_Put) -> HTTPException:
    req: dict = await request.json()
    user_name = req.get("user_name")
    user_email = req.get("user_email")
    if not await get_uid_check_exist(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    if user_name and user_name is None:
        raise HTTPException(status_code=400, detail=f"Nothing to update")

    if not user_name:
        user_name = await get_user_name_by_uid(uid)

    if not user_email:
        user_email = await get_user_email_by_uid(uid)

    if await put_user_info(uid, user_name, user_email):
        raise HTTPException(status_code=404, detail=f"Profile dont update")

    raise HTTPException(status_code=200, detail=f"OK")
