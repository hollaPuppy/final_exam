from fastapi import APIRouter, \
                    Request
from fastapi.responses import UJSONResponse
from datetime import datetime
from .schemas.lobbies import Lobbies_New, \
                             Lobbies_Get_In, \
                             Lobbies_Get_Out, \
                             Lobbies_Put_Cap
from ..queries.queries_lobbies import get_lob_list, \
                                      get_lob_pass, \
                                      get_lob_fullness, \
                                      get_lob_id, \
                                      get_lob_usr_count, \
                                      get_lob_usr_is_cap, \
                                      get_lob_usr_id, \
                                      post_lob, \
                                      post_lob_usr, \
                                      put_lob_usr_role, \
                                      delete_lob_usr, \
                                      delete_lob
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
    await post_lob(lob_is_closed, lob_pass_code, lob_name, lob_create_date)
    lod_id = await get_lob_id(lob_name, lob_create_date)
    await post_lob_usr(uid, 1, lod_id)

    return UJSONResponse({"lob_id": lod_id, "lob_pass_code": lob_pass_code})


@routerLobbies.post("/get/in")
async def connect_to_lobby(request: Request, body: Lobbies_Get_In) -> str:
    req: dict = await request.json()
    lob_id = req.get("lob_id")
    lob_pass_code = req.get("lob_pass_code")
    uid = req.get("uid")
    if lob_pass_code != await get_lob_pass(lob_id):
        if lob_pass_code is None:
            return f"Missing password"
        else:
            return f"Wrong pass code"
    if await get_lob_fullness(lob_id):
        return f"Lobby already filled"
    await post_lob_usr(uid, 0, lod_id)
    await put_lob_fullness(lob_id)

    return "ok"


@routerLobbies.post("/get/out")
async def disconnect_from_lobby(request: Request, body: Lobbies_Get_In) -> str:
    req: dict = await request.json()
    lob_id = req.get("lob_id")
    uid = req.get("uid")
    cap_flag = await get_lob_usr_is_cap(uid, lob_id)
    await delete_lob_usr(uid, lob_id)
    if await get_lob_usr_count(lob_id) == 0:
        await delete_lob(lob_id)
        return f"Since the lobby became empty it was removed"
    else:
        if cap_flag:
            second_uid = await get_lob_usr_id(lob_id)
            await put_lob_usr_role(second_uid, true, lob_id)
    return f"Capitan switched"


# _______________PUT___________

@routerLobbies.put("/put/cap")
async def put_lobby_cap(request: Request, body: Lobbies_Put_Cap) -> str:
    req: dict = await request.json()
    lob_id = req.get("lob_id")
    cap_uid = await get_lob_usr_id(lob_id, true)
    second_uid = await get_lob_usr_id(lob_id, false)
    await put_lob_usr_role(cap_uid, false, lob_id)
    await put_lob_usr_role(second_uid, true, lob_id)
    return f"Capitan switched"
