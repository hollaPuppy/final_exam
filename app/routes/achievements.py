from fastapi import APIRouter, \
                    Request, \
                    HTTPException
from fastapi.responses import UJSONResponse
from ..queries.queries_achievements import get_check_achievement, \
                                           get_achievements_list, \
                                           get_limit_achievements_list, \
                                           get_complete_achievements_list, \
                                           get_complete_achievements_by_username, \
                                           get_process_achievements_by_username, \
                                           get_achievement_id, \
                                           post_achievement, \
                                           post_process_achievement, \
                                           post_complete_achievement, \
                                           put_achievement, \
                                           put_process_achievement
from ..queries.queries_users import get_check_username_exist, \
                                    get_check_user_by_uid
from .schemas.achievements import Achievements_New, \
                                  Achievements_Process_New, \
                                  Achievements_Complete_New, \
                                  Achievements_Put, \
                                  Achievements_Process_Put
from datetime import datetime

routerAchievements = APIRouter(
    prefix='/achievements',
    tags=['achievements']
)


@routerAchievements.get("/all")
async def achievements_list() -> UJSONResponse:
    response = await get_achievements_list()
    if not response:
        raise HTTPException(status_code=404, detail=f"Achievements not found")

    return UJSONResponse({'achieves': response})


@routerAchievements.get("/all_limit")
async def limit_achievements_list() -> UJSONResponse:
    response = await get_limit_achievements_list()
    if not response:
        raise HTTPException(status_code=404, detail=f"Limit achievements not found")
    return UJSONResponse({'limit_achieves': response})


@routerAchievements.get("/complete/{username}")
async def complete_achievements_list(username: str) -> UJSONResponse:
    if username == 'all':
        response = await get_complete_achievements_list()
    else:
        if not await get_check_username_exist(username):
            raise HTTPException(status_code=404, detail=f"User {username} not found")

        response = await get_complete_achievements_by_username(username)
        if not response:
            raise HTTPException(status_code=404, detail=f"Complete achievements for {username} not found")

    return UJSONResponse({'complete_achieves': response})


@routerAchievements.get("/process/{username}")
async def process_achievements_list(username: str) -> UJSONResponse:
    if username == 'all':
        response = await get_process_achievements_list()
    else:
        if not await get_check_username_exist(username):
            raise HTTPException(status_code=404, detail=f"User {username} not found")

        response = await get_process_achievements_by_username(username)
        if not response:
            raise HTTPException(status_code=404, detail=f"Process achievements for {username} not found")

    return UJSONResponse({'process_achieves': response})


# _______________POST___________


@routerAchievements.post("/new")
async def new_achievement(request: Request, body: Achievements_New) -> str:
    req: dict = await request.json()
    achv_name = req.get("achv_name")
    achv_req = req.get("achv_req")
    achv_is_limit = req.get("achv_is_limit")
    achv_date_end_if_limit = req.get("achv_date_end_if_limit")

    if not await post_achievement(achv_name, achv_req, achv_is_limit, achv_date_end_if_limit):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    achv_id = get_achievement_id(achv_name, achv_req)

    return HTTPException(status_code=200, detail=f"{achv_id}")


@routerAchievements.post("/process/new")
async def new_process_achievement(request: Request, body: Achievements_Process_New) -> str:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    uid = req.get("uid")
    achv_pass = req.get("achv_pass")

    if not await get_check_user_by_uid(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    if not await post_process_achievement(achv_id, uid, achv_pass):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


@routerAchievements.post("/complete/new")
async def new_complete_achievement(request: Request, body: Achievements_Complete_New) -> str:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    uid = req.get("uid")
    achv_receive_date = req.get("achv_receive_date")
    if not achv_receive_date:
        achv_receive_date = datetime.now()

    if not await get_check_user_by_uid(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    if not await post_complete_achievement(achv_id, uid, achv_receive_date):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


# _______________PUT___________


@routerAchievements.put("/put")
async def put_achievement(request: Request, body: Achievements_Put) -> str:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    achv_name = req.get("achv_name")
    achv_req = req.get("uid")
    achv_is_limit = req.get("achv_receive_date")
    achv_date_end_if_limit = req.get("achv_receive_date")
    if not get_check_achievement(achv_id):
        raise HTTPException(status_code=404, detail=f"Achievement with id {achv_id} not found")

    if not await put_achievement(achv_id, achv_name, achv_req, achv_is_limit, achv_date_end_if_limit):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


@routerAchievements.put("/process/put")
async def put_achievement(request: Request, body: Achievements_Process_Put) -> str:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    uid = req.get("uid")
    achv_pass = req.get("achv_pass")
    if not get_check_achievement(achv_id):
        raise HTTPException(status_code=404, detail=f"Achievement with id {achv_id} not found")

    if not await get_check_user_by_uid(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    if not await put_process_achievement(achv_id, uid, achv_pass):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


# _______________DELETE___________
