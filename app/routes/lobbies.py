from fastapi import APIRouter, \
                    Request, \
                    HTTPException
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
                                      put_lob_fullness, \
                                      delete_lob_usr, \
                                      delete_lob
from ..utils.lobbies import gen_pass_code

routerLobbies = APIRouter(
    prefix='/lobbies',
    tags=['lobbies']
)


@routerLobbies.get("/all")
async def lobbies_list() -> UJSONResponse:
    response = await get_lob_list()
    if not response:
        raise HTTPException(status_code=404, detail=f"Lobbies not found")

    return UJSONResponse({'lobbies': response})


@routerLobbies.post("/new")
async def new_lobby(request: Request, body: Lobbies_New) -> HTTPException:
    lob_pass_code = ''
    lob_create_date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    req: dict = await request.json()
    lob_is_closed = req.get("lob_is_closed")
    lob_name = req.get("lob_name")
    uid = req.get("uid")
    if lob_is_closed:
        lob_pass_code = gen_pass_code()

    await post_lob(lob_is_closed, lob_pass_code, lob_name, lob_create_date)
    lod_id = await get_lob_id(lob_name, lob_create_date)
    await post_lob_usr(uid, True, lod_id)
    # Добавить исключений
    return HTTPException(status_code=200, detail=f"OK")


@routerLobbies.post("/get/in")
async def connect_to_lobby(request: Request, body: Lobbies_Get_In) -> HTTPException:
    req: dict = await request.json()
    lob_id = req.get("lob_id")
    lob_pass_code = req.get("lob_pass_code")
    uid = req.get("uid")
    if lob_pass_code != await get_lob_pass(lob_id):
        if lob_pass_code is None:
            raise HTTPException(status_code=404, detail=f"Password not found")
        else:
            raise HTTPException(status_code=400, detail=f"Wrong password")

    if await get_lob_fullness(lob_id):
        raise HTTPException(status_code=400, detail=f"Lobby already filled")

    await post_lob_usr(uid, False, lob_id)
    await put_lob_fullness(lob_id)

    return HTTPException(status_code=200, detail=f"OK")


@routerLobbies.post("/get/out")
async def disconnect_from_lobby(request: Request, body: Lobbies_Get_In) -> HTTPException:
    req: dict = await request.json()
    lob_id = req.get("lob_id")
    uid = req.get("uid")
    cap_flag = await get_lob_usr_is_cap(uid, lob_id)
    await delete_lob_usr(uid, lob_id)

    if await get_lob_usr_count(lob_id) == 0:
        if await delete_lob(lob_id) is not None:
            raise HTTPException(status_code=501, detail=f"Write to database failed")
        return HTTPException(status_code=200, detail=f"Since the lobby became empty it was removed")

    else:
        if cap_flag:
            second_uid = await get_lob_usr_id(lob_id)

            if await put_lob_usr_role(second_uid, True, lob_id) is not None:
                raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"Capitan switched")


@routerLobbies.put("/put/cap")
async def put_lobby_cap(request: Request, body: Lobbies_Put_Cap) -> HTTPException:
    req: dict = await request.json()
    lob_id = req.get("lob_id")
    cap_uid = await get_lob_usr_id(lob_id, True)
    second_uid = await get_lob_usr_id(lob_id, False)

    if await put_lob_usr_role(cap_uid, False, lob_id) or await put_lob_usr_role(second_uid, true, lob_id) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"Capitan switched")
