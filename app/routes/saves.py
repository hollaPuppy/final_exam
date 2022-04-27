from fastapi import APIRouter, Request
from fastapi.responses import UJSONResponse

from ..queries.queries_saves import create_save_record, \
                                    get_save_record_id, \
                                    create_puz_records, \
                                    create_coords_records, \
                                    update_coords_records, \
                                    get_saves_by_username, \
                                    get_coords_by_save_id, \
                                    get_complete_puzzles_list

from .schemas.saves import Saves_Set_New, Saves_Full_Info
from ..utils.saves import create_puz_id_list

routerSave = APIRouter(
    prefix='/save',
    tags=['save']
)


@routerSave.post("/new_save")
async def set_save(request: Request, body: Saves_Set_New) -> str:
    req: dict = await request.json()
    username = req.get("username")
    save_name = req.get("save_name")
    coord_pos = req.get("coord_pos")
    coord_rot = req.get("coord_rot")
    puz_id_list = req.get("puz_id_list")

    if await create_save_record(username, save_name) != f"ok":
        return 'Some bad with create save record'
    save_record_id = await get_save_record_id(username, save_name)
    puz_id_list = create_puz_id_list(int(save_record_id), puz_id_list)
    await create_puz_records(puz_id_list)
    await create_coords_records(coord_pos, coord_rot, int(save_record_id))
    return f"all good"


@routerSave.post("/update_save")
async def set_save(request: Request, body: Saves_Set_New) -> str:
    req: dict = await request.json()
    username = req.get("username")
    save_name = req.get("save_name")
    coord_pos = req.get("coord_pos")
    coord_rot = req.get("coord_rot")
    puz_id_list = req.get("puz_id_list")

    save_record_id = await get_save_record_id(username, save_name)
    puz_id_list = create_puz_id_list(int(save_record_id), puz_id_list)
    await create_puz_records(puz_id_list)
    await update_coords_records(coord_pos, coord_rot, int(save_record_id))
    return f"all good"


@routerSave.get("/list/{username}")
async def saves_list(username: str) -> UJSONResponse:
    response = await get_saves_by_username(username)

    return UJSONResponse({'saves': response})


@routerSave.get("/full_info")
async def saves_list(request: Request, body: Saves_Full_Info) -> UJSONResponse:
    req: dict = await request.json()
    save_name = req.get("save_name")
    username = req.get("username")
    save_record_id = await get_save_record_id(username, save_name)
    response_coords = await get_coords_by_save_id(int(save_record_id))
    com_puz_lst = await get_complete_puzzles_list(38)
    com_puz_str = ";".join(map(lambda row:str((row.get('puz_id'))), com_puz_lst))
    return UJSONResponse({"coords": response_coords, "complete_puzzles": com_puz_str})