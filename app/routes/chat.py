from fastapi import APIRouter, \
                    WebSocket
from ..utils.sockets import SocketManager
from ..queries.queries_users import get_uid_by_username
routerChat = APIRouter(
    prefix='/chat',
    tags=['chat']
)

manager = SocketManager()


@routerChat.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, uid: int):
    await manager.connect(websocket)
    await websocket.accept()
    user_name = get_username_by_uid(uid)
    while True:
        try:
            data = await websocket.receive_text()
            print(data)
        except RuntimeError:
            break
        await manager.broadcast(f"{user_name} wrote: {data}")



