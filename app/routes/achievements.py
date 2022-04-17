from fastapi import APIRouter, Request
from fastapi.responses import UJSONResponse

from .schemas.schemas import Achievements_List_Get
from ..queries.queries_achievements import get_achievements_list, get_limit_achievements_list


routerAchievements = APIRouter(
    prefix='/achievements',
    tags=['achievements']
)


# @routerAchievements.get("/all")
# async def achievements_list() -> list:
#     response = await get_achievements_list()
#     listik = list(map(lambda row: Achievements_List_Get(**row).dict(), response))
#     for item in listik:
#         print(item[' '])
#     print(listik)
#     print(type(listik))
#     return list(map(lambda row: Achievements_List_Get(**row).dict(), response))


@routerAchievements.get("/all")
async def achievements_list() -> UJSONResponse:
    response = await get_achievements_list()
    return UJSONResponse({'achieves': response})


@routerAchievements.get("/all_limit")
async def limit_achievements_list() -> UJSONResponse:
    response = await get_limit_achievements_list()
    return  UJSONResponse({'achieves': response})


# @routerAchievements.post("/new")
# def getAchievementsList(model: achievements_list,
#                         name_ach: str,
#                         req_ach: int,
#                         limit_ach: bool,
#                         date_end_if_limit_ach: str):
#     return {"Ok"}
#

