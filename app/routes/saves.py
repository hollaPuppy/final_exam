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
                                    post_save_record, \
                                    put_coords_records
from .schemas.saves import Saves_Set_New, \
                           Saves_Full_Info
from ..utils.saves import create_puz_id_list

routerSave = APIRouter(
    prefix='/saves',
    tags=['saves']
)


@routerSave.get("/list/{username}")
async def saves_list(user_name: str) -> UJSONResponse:
    response = await get_saves_by_username(user_name)
    if not response:
        raise HTTPException(status_code=404, detail=f"Saves for {user_name} not found")
    return UJSONResponse({'saves': response})


@routerSave.get("/full_info")
async def saves_list(request: Request, body: Saves_Full_Info) -> UJSONResponse:
    req: dict = await request.json()
    save_name = req.get("save_name")
    user_name = req.get("user_name")
    save_record_id = await get_save_record_id(user_name, save_name)
    if not save_record_id:
        raise HTTPException(status_code=404, detail=f"Saves for {user_name} not found")
    response_coords = await get_coords_by_save_id(int(save_record_id))
    com_puz_lst = await get_complete_puzzles_list(int(save_record_id))
    com_puz_str = ";".join(map(lambda row: str(row.get('puz_id')), com_puz_lst))

    return UJSONResponse({"coords": response_coords, "complete_puzzles": com_puz_str})


@routerSave.post("/new")
async def set_save(request: Request, body: Saves_Set_New) -> HTTPException:
    req: dict = await request.json()
    user_name = req.get("user_name")
    save_name = req.get("save_name")
    coord_pos = req.get("coord_pos")
    coord_rot = req.get("coord_rot")
    puz_id_list = req.get("puz_id_list")
    if await post_save_record(user_name, save_name) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    save_record_id = await get_save_record_id(user_name, save_name)
    if not save_record_id:
        raise HTTPException(status_code=404, detail=f"Save {save_name} for {user_name} not found")
    puz_id_list = create_puz_id_list(int(save_record_id), puz_id_list)

    if await post_puz_records(puz_id_list) \
            or await post_coords_records(coord_pos, coord_rot, int(save_record_id)) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


@routerSave.post("/put")
async def set_save(request: Request, body: Saves_Set_New) -> HTTPException:
    req: dict = await request.json()
    user_name = req.get("user_name")
    save_name = req.get("save_name")
    coord_pos = req.get("coord_pos")
    coord_rot = req.get("coord_rot")
    puz_id_list = req.get("puz_id_list")

    save_record_id = await get_save_record_id(user_name, save_name)
    if not save_record_id:
        raise HTTPException(status_code=404, detail=f"Save {save_name} for {user_name} not found")
    puz_id_list = create_puz_id_list(int(save_record_id), puz_id_list)

    if await post_puz_records(puz_id_list) \
            or await put_coords_records(coord_pos, coord_rot, int(save_record_id)) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")


