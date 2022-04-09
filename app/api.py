from fastapi import FastAPI
from app.routes import login_auth, achievements
from .database import SessionLocal, engine
from . import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='backend for PC video-game')
app.include_router(login_auth.routerLogin)
app.include_router(achievements.routerAchievements)





