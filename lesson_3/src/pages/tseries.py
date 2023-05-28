from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request

tseries_router = APIRouter()

templates = Jinja2Templates(directory="templates")


@tseries_router.get("/tseries")
async def get_tseries_page(request: Request):
    return templates.TemplateResponse("tseries.html",
                                      {"request": request})
