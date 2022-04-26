from fastapi import APIRouter, Request

from ..queries.queries_saves import create_save_record, \
                                    get_save_record_id, \
                                    create_puz_records, \
                                    create_coord_records

from datetime import datetime
from .schemas.saves import Saves_Set_New
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
    await create_coord_records(coord_pos, coord_rot, int(save_record_id))
    return f"all good"
