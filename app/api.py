from fastapi import FastAPI
from app.routes import login, achievements, saves
import sqlalchemy
from .db import DB

metadata = sqlalchemy.MetaData()

app = FastAPI(title='backend for PC video-game')
app.include_router(login.routerUser)
app.include_router(achievements.routerAchievements)
app.include_router(saves.routerSave)


@app.on_event("startup")
async def startup() -> None:
    await DB.connect()


@app.on_event("shutdown")
async def shutdown():
    await DB.close()









