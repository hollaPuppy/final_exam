from fastapi import APIRouter, \
                    Request
from fastapi.responses import UJSONResponse
from datetime import datetime
from .schemas.notifications import Notifications_List, \
                                   Notifications_Post_New, \
                                   Notifications_Put_Opened
from ..queries.queries_notifications import get_ntfct_list_by_username, \
                                            get_ntfct_id_by_title_text_date, \
                                            post_ntfct_for_user, \
                                            post_ntfct_for_all, \
                                            post_ntfct_body
from ..utils.notifications import get_list_uids_and_ntfct


routerNotifications = APIRouter(
    prefix='/notifications',
    tags=['notifications']
)


@routerNotifications.get("/all/{username}")
async def notifications_list(username: str) -> UJSONResponse:
    response = await get_ntfct_list_by_username(username)
    return UJSONResponse({'notifications': response})


@routerNotifications.post("/new/{username}")
async def notifications_post(username: str, request: Request, body: Notifications_Post_New) -> str:
    req: dict = await request.json()
    ntfct_title = req.get("ntfct_title")
    ntfct_text = req.get("ntfct_text")
    ntfct_date = req.get("ntfct_date")
    if ntfct_date == "":
        ntfct_date = datetime.now()
    await post_ntfct_body(ntfct_title, ntfct_text, ntfct_date)
    ntfct_id = await get_ntfct_id_by_title_text_date(ntfct_title, ntfct_text, ntfct_date)

    await get_list_uids_and_ntfct(ntfct_id, username)
    return f"{ntfct_id}"


@routerNotifications.put("/open/{username}")
async def notifications_post(username: str, body: Notifications_Put_Opened) -> str:
    req: dict = await request.json()
    ntfct_id = req.get("ntfct_id")
    username = req.get("username")


