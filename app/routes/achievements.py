from fastapi import APIRouter, Request
from fastapi.responses import UJSONResponse
from ..queries.queries_achievements import get_achievements_list, get_limit_achievements_list
from app.routes.schemas.schemas import achievements_list


routerAchievements = APIRouter(
    prefix='/achievements',
    tags=['achievements']
)


@routerAchievements.get("/all")
async def achievements_list() -> list:
    response = await get_achievements_list()
    return response


@routerAchievements.get("/all_limit")
async def limit_achievements_list() -> list:
    response = await get_limit_achievements_list()
    return response


# @routerAchievements.post("/new")
# def getAchievementsList(model: achievements_list,
#                         name_ach: str,
#                         req_ach: int,
#                         limit_ach: bool,
#                         date_end_if_limit_ach: str):
#     return {"Ok"}
#

