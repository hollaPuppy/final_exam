from fastapi import APIRouter, \
                    Request, \
                    HTTPException
from fastapi.responses import UJSONResponse
from datetime import datetime
from .schemas.notifications import Notifications_List, \
                                   Notifications_Post_New, \
                                   Notifications_Put_Opened
from ..queries.queries_notifications import get_ntfct_list_by_username, \
                                            get_ntfct_id_by_title_text_date, \
                                            post_ntfct_body, \
                                            put_ntfct_for_user
from ..queries.queries_users import get_check_username_exist
from ..utils.notifications import get_list_uids_and_ntfct


routerNotifications = APIRouter(
    prefix='/notifications',
    tags=['notifications']
)


@routerNotifications.get("/all/{username}")
async def notifications_list(username: str) -> UJSONResponse:
    response = await get_ntfct_list_by_username(username)
    if not response:
        raise HTTPException(status_code=404, detail=f"Notifications for {username} not found")

    return UJSONResponse({'notifications': response})


@routerNotifications.post("/new/{user_name}")
async def notifications_post(user_name: str, request: Request, body: Notifications_Post_New) -> HTTPException:
    req: dict = await request.json()
    ntfct_title = req.get("ntfct_title")
    ntfct_text = req.get("ntfct_text")
    ntfct_date = req.get("ntfct_date")
    if not await get_check_username_exist(user_name):
        raise HTTPException(status_code=404, detail=f"User {user_name} not found")

    if ntfct_date == "":
        ntfct_date = datetime.now()

    if await post_ntfct_body(ntfct_title, ntfct_text, ntfct_date) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    ntfct_id = await get_ntfct_id_by_title_text_date(ntfct_title, ntfct_text, ntfct_date)

    if not await get_list_uids_and_ntfct(ntfct_id, user_name):
        raise HTTPException(status_code=501, detail=f"Write to database failed")
    # кринж все переделать
    return HTTPException(status_code=200, detail=f"{ntfct_id}")


@routerNotifications.put("/open/")
async def notifications_post(request: Request, body: Notifications_Put_Opened) -> HTTPException:
    req: dict = await request.json()
    ntfct_id = req.get("ntfct_id")
    user_name = req.get("user_name")
    if not await get_check_username_exist(user_name):
        raise HTTPException(status_code=404, detail=f"User {user_name} not found")

    if await put_ntfct_for_user(ntfct_id, user_name) is not None:
        raise HTTPException(status_code=501, detail=f"Write to database failed")

    return HTTPException(status_code=200, detail=f"OK")
