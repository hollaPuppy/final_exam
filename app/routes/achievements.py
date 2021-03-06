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
                                           get_process_achievements_list, \
                                           get_achievement_id, \
                                           post_achievement, \
                                           post_process_achievement, \
                                           post_complete_achievement, \
                                           put_achievement, \
                                           put_process_achievement
from ..queries.queries_users import get_user_name_check_exist, \
                                    get_user_by_uid_check
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


@routerAchievements.get("/complete/{user_name}")
async def complete_achievements_list(user_name: str) -> UJSONResponse:
    if user_name == 'all':
        response = await get_complete_achievements_list()
    else:
        if not await get_user_name_check_exist(user_name):
            raise HTTPException(status_code=404, detail=f"User {user_name} not found")

        response = await get_complete_achievements_by_username(user_name)
        if not response:
            raise HTTPException(status_code=404, detail=f"Complete achievements for {user_name} not found")

    return UJSONResponse({'complete_achieves': response})


@routerAchievements.get("/process/{user_name}")
async def process_achievements_list(user_name: str) -> UJSONResponse:
    if user_name == 'all':
        response = await get_process_achievements_list()
    else:
        if not await get_user_name_check_exist(user_name):
            raise HTTPException(status_code=404, detail=f"User {user_name} not found")

        response = await get_process_achievements_by_username(user_name)
        if not response:
            raise HTTPException(status_code=404, detail=f"Process achievements for {user_name} not found")

    return UJSONResponse({'process_achieves': response})


# _______________POST___________


@routerAchievements.post("/new")
async def new_achievement(request: Request, body: Achievements_New) -> HTTPException:
    req: dict = await request.json()
    achv_name = req.get("achv_name")
    achv_req = req.get("achv_req")
    achv_is_limit = req.get("achv_is_limit")
    achv_date_end_if_limit = req.get("achv_date_end_if_limit")

    if post_achievement(achv_name, achv_req, achv_is_limit, achv_date_end_if_limit) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    achv_id = get_achievement_id(achv_name, achv_req)

    return HTTPException(status_code=200, detail=f"{achv_id}")


@routerAchievements.post("/process/new")
async def new_process_achievement(request: Request, body: Achievements_Process_New) -> HTTPException:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    uid = req.get("uid")
    achv_pass = req.get("achv_pass")

    if not await get_check_user_by_uid(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    if post_process_achievement(achv_id, uid, achv_pass) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


@routerAchievements.post("/complete/new")
async def new_complete_achievement(request: Request, body: Achievements_Complete_New) -> HTTPException:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    uid = req.get("uid")
    achv_receive_date = req.get("achv_receive_date")
    if not achv_receive_date:
        achv_receive_date = datetime.now()

    if not await get_check_user_by_uid(uid):
        raise HTTPException(status_code=404, detail=f"User with uid {uid} not found")

    if post_complete_achievement(achv_id, uid, achv_receive_date) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


@routerAchievements.put("/put")
async def put_achievement(request: Request, body: Achievements_Put) -> HTTPException:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    achv_name = req.get("achv_name")
    achv_req = req.get("uid")
    achv_is_limit = req.get("achv_receive_date")
    achv_date_end_if_limit = req.get("achv_receive_date")
    if not get_check_achievement(achv_id):
        raise HTTPException(status_code=404, detail=f"Achievement with id {achv_id} not found")

    if put_achievement(achv_id, achv_name, achv_req, achv_is_limit, achv_date_end_if_limit) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


@routerAchievements.put("/process/put")
async def put_achievement(request: Request, body: Achievements_Process_Put) -> HTTPException:
    req: dict = await request.json()
    achv_id = req.get("achv_id")
    uid = req.get("uid")
    achv_pass = req.get("achv_pass")
    if not await get_check_achievement(achv_id) or await get_check_user_by_uid(uid):
        raise HTTPException(status_code=404, detail=f"Record not found")

    if put_process_achievement(achv_id, uid, achv_pass) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")
