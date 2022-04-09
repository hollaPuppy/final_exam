from fastapi import APIRouter
from app.schemas import achievements_list, process_achievements, complete_achievements

routerAchievements = APIRouter(
    prefix='/achievements',
    tags=['achievements']
)


@routerAchievements.get("/all")
def getAchievementsList(model: achievements_list):
    return {'data': model}


@routerAchievements.post("/new")
def getAchievementsList(model: achievements_list,
                        name_ach: str,
                        req_ach: int,
                        limit_ach: bool,
                        date_end_if_limit_ach: str):
    return {"Ok"}

