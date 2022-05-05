from fastapi import APIRouter, \
                    Request, \
                    HTTPException
from fastapi.responses import UJSONResponse
from ..queries.queries_saves import get_saves_by_username, \
                                    get_coords_by_save_id, \
                                    get_complete_puzzles_list, \
                                    get_save_record_id, \
                                    post_puz_records, \
                                    post_coords_records, \
                                    post_save_record
from .schemas.saves import Saves_Set_New, \
                           Saves_Full_Info
from ..utils.saves import create_puz_id_list

routerSave = APIRouter(
    prefix='/saves',
    tags=['saves']
)


@routerSave.get("/list/{username}")
async def saves_list(username: str) -> UJSONResponse:
    response = await get_saves_by_username(username)
    if not response:
        raise HTTPException(status_code=404, detail=f"Saves for {username} not found")
    return UJSONResponse({'saves': response})


@routerSave.get("/full_info")
async def saves_list(request: Request, body: Saves_Full_Info) -> UJSONResponse:
    req: dict = await request.json()
    save_name = req.get("save_name")
    username = req.get("username")
    save_record_id = await get_save_record_id(username, save_name)
    if not save_record_id:
        raise HTTPException(status_code=404, detail=f"Saves for {username} not found")
    response_coords = await get_coords_by_save_id(int(save_record_id))
    com_puz_lst = await get_complete_puzzles_list(save_record_id)
    com_puz_str = ";".join(map(lambda row: str(row.get('puz_id')), com_puz_lst))

    return UJSONResponse({"coords": response_coords, "complete_puzzles": com_puz_str})


# _______________POST___________


@routerSave.post("/new")
async def set_save(request: Request, body: Saves_Set_New) -> str:
    req: dict = await request.json()
    username = req.get("username")
    save_name = req.get("save_name")
    coord_pos = req.get("coord_pos")
    coord_rot = req.get("coord_rot")
    puz_id_list = req.get("puz_id_list")
    if not post_save_record(username, save_name):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    save_record_id = await get_save_record_id(username, save_name)
    if not save_record_id:
        raise HTTPException(status_code=404, detail=f"Save {save_name} for {username} not found")

    puz_id_list = await create_puz_id_list(int(save_record_id), puz_id_list)

    if not await post_puz_records(puz_id_list):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    if not await post_coords_records(coord_pos, coord_rot, int(save_record_id)):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


# _______________PUT___________


@routerSave.post("/put")
async def set_save(request: Request, body: Saves_Set_New) -> str:
    req: dict = await request.json()
    username = req.get("username")
    save_name = req.get("save_name")
    coord_pos = req.get("coord_pos")
    coord_rot = req.get("coord_rot")
    puz_id_list = req.get("puz_id_list")

    save_record_id = await get_save_record_id(username, save_name)
    if not save_record_id:
        raise HTTPException(status_code=404, detail=f"Save {save_name} for {username} not found")
    puz_id_list = await create_puz_id_list(int(save_record_id), puz_id_list)

    if not await post_puz_records(puz_id_list):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    if not await update_coords_records(coord_pos, coord_rot, int(save_record_id)):
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


