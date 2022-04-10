from fastapi import FastAPI
from app.routes import login_auth, achievements
from .schemas import users
import databases
import sqlalchemy
from .db import DB


DATABASE_URL = "postgresql://faozuispekgops:49e44fdedf916d54c5d562385a7677a6f387af7111403befac06fa0b2f96c73b@ec2-176" \
               "-34-116-203.eu-west-1.compute.amazonaws.com:5432/d1gec1g9j9v7sr"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

app = FastAPI(title='backend for PC video-game')
app.include_router(login_auth.routerUser)
# app.include_router(achievements.routerAchievements)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={}
)
metadata.create_all(engine)


@app.on_event("startup")
async def startup() -> None:
    await DB.connect()


@app.on_event("shutdown")
async def shutdown():
    await DB.close()









