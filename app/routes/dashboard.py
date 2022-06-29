from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from routes.videos import search_videos

dashboard = APIRouter()

templates = Jinja2Templates(directory="templates")


@dashboard.get("/")
async def show_dashboard(
    request: Request,
    query: str = None
):
    videos = await search_videos(query, limit=100, offset=0)
    return templates.TemplateResponse(
        "dashboard.jinja",
        {"videos": videos, "request": request}
    )
