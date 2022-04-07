from fastapi import APIRouter

routerLogin = APIRouter(
    prefix='/login',
    tags=['login']
)


@routerLogin.get("/")
def index():
    return {"Hello! You are welcome here! There is backend for video-game '%game_name%'"}


@routerLogin.get("achievements_all")
def get_all_ach():
    return {"Hello! You are welcome here! There is backend for video-game '%game_name%'"}