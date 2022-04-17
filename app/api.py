from fastapi import FastAPI
from app.routes import login, achievements
import sqlalchemy
from .db import DB

metadata = sqlalchemy.MetaData()

app = FastAPI(title='backend for PC video-game')
app.include_router(login.routerUser)
app.include_router(achievements.routerAchievements)


@app.on_event("startup")
async def startup() -> None:
    await DB.connect()


@app.on_event("shutdown")
async def shutdown():
    await DB.close()









