from fastapi import APIRouter, Request
from fastapi.responses import UJSONResponse
from datetime import datetime

from .schemas.lobbies import Lobbies_New, \
    Lobbies_Get_In
from ..queries.queries_lobbies import get_lobbies_list, \
    post_lobby, \
    post_cap_lobby
from ..utils.lobbies import gen_pass_code

routerLobbies = APIRouter(
    prefix='/lobbies',
    tags=['lobbies']
)


@routerLobbies.get("/all")
async def lobbies_list() -> UJSONResponse:
    response = await get_lobbies_list()
    return UJSONResponse({'lobbies': response})


# _______________POST___________

@routerLobbies.post("/new")
async def new_lobby(request: Request, body: Lobbies_New) -> UJSONResponse:
    lob_pass_code = ''
    lob_create_date = datetime.now()
    req: dict = await request.json()
    lob_is_closed = req.get("lob_is_closed")
    lob_name = req.get("lob_name")
    uid = req.get("uid")
    if lob_is_open:
        lob_pass_code = gen_pass_code()
    await post_lobby(lob_is_closed, lob_pass_code, lob_name, lob_create_date)
    lod_id = await get_created_lobby(lob_name, lob_create_date)
    await post_cap_lobby(uid, lod_id)

    return UJSONResponse({"lob_id": lod_id, "lob_pass_code": lob_pass_code})


@routerLobbies.post("/get/in")
async def connect_to_lobby(request: Request, body: Lobbies_Get_In) -> str:
    req: dict = await request.json()
    lob_id = req.get("lob_id")
    lob_pass_code = req.get("lob_pass_code")
    uid = req.get("uid")
    print(lob_id, lob_pass_code, uid)
    if lob_pass_code is None:
        print('That is open lobby')
    # нужно: проверять открытость лобби, заполненность, сверить коды доступа, подумать что делать, если приходит пустой
    # пароль и какой-то, добавлять записьв лоб_юз, менять флаг заполненности
    return "ok"


@routerLobbies.post("/get/out")
async def disconnect_from_lobby(request: Request, body: Lobbies_New) -> str:
    sm = 'sm'
    # проверять кто вышел - кэп или простой, если кэп - пекредавать флаг кэпа, если нет - просто удалять запись в лоб_эз
    # затем проверять кол-во записей вс лоб_юзерс - 0=удалять запись из лобис