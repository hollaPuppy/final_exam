from fastapi import APIRouter, Request

from ..queries.queries_saves import create_save_record

from datetime import datetime


routerSave = APIRouter(
    prefix='/save',
    tags=['save']
)


@routerSave.post("/new_save")
async def reg(request: Request) -> str:
    req: dict = await request.json()
    username = req.get("username")
    save_name = req.get("save_name")
    await create_save_record(username, save_name)
    # запихнуть инсерт в трай, после создания дергать айдишник послдней записи (по юиду и максимальной дате)
    # затем создать запись в координатах с айдишником, затем создать список пройденыз пазлов с тем же айдишником
    return test
