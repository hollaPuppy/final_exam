from fastapi import FastAPI
from app.routes import users, \
                       achievements, \
                       saves, \
                       lobbies, \
                       notifications, \
                       admin
from .db import DB
from fastapi.staticfiles import StaticFiles


app = FastAPI(title='backend for PC video-game')
app.include_router(users.routerUser)
app.include_router(achievements.routerAchievements)
app.include_router(saves.routerSave)
app.include_router(lobbies.routerLobbies)
app.include_router(notifications.routerNotifications)
app.include_router(admin.routerAdmin)

app.mount("/static", StaticFiles(directory="app/templates"), name="static")


@app.on_event("startup")
async def startup() -> None:
    await DB.connect()


@app.on_event("shutdown")
async def shutdown():
    await DB.close()









