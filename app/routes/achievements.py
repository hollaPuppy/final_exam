from fastapi import APIRouter, Request
from fastapi.responses import UJSONResponse
from ..queries.queries_achievements import get_achievements_list, \
                                           get_limit_achievements_list, \
                                           get_complete_achievements_list, \
                                           get_complete_achievements_by_username, \
                                           post_achievement
from .schemas.achievements import Achievements_New


routerAchievements = APIRouter(
    prefix='/achievements',
    tags=['achievements']
)


@routerAchievements.get("/all")
async def achievements_list() -> UJSONResponse:
    response = await get_achievements_list()
    return UJSONResponse({'achieves': response})


@routerAchievements.get("/all_limit")
async def limit_achievements_list() -> UJSONResponse:
    response = await get_limit_achievements_list()
    return UJSONResponse({'limit_achieves': response})


@routerAchievements.get("/complete/{username}")
async def complete_achievements_list(username: str) -> UJSONResponse:
    if username == 'all':
        response = await get_complete_achievements_list()
    else:
        response = await get_complete_achievements_by_username(username)

    return UJSONResponse({'complete_achieves': response})


@routerAchievements.get("/process/{username}")
async def complete_achievements_list(username: str) -> UJSONResponse:
    if username == 'all':
        response = await get_process_achievements_list()
    else:
        response = await get_process_achievements_by_username(username)

    return UJSONResponse({'process_achieves': response})

# _______________POST___________


@routerAchievements.post("/new")
async def new_achievement(request: Request, body: Achievements_New) -> str:
    await post_achievement(request)
    return "ok"

