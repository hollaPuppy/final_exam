from fastapi import FastAPI, \
                    Request, \
                    APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")


routerAdmin = APIRouter(
    prefix='/web-admin',
    tags=['web-admin']
)


@routerAdmin.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

