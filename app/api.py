from fastapi import FastAPI
from app.routes import login_auth

app = FastAPI(title='backend for PC video-game')
app.include_router(login_auth.routerLogin)



