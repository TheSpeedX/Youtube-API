from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pymongo import TEXT
from routes.videos import videos
from routes.dashboard import dashboard
from tasks.scrapper import run_scrapper_task
from config.database import db
from config.variables import SEARCH_QUERY, REFRESH_INTERVAL, API_KEYS
import asyncio


app = FastAPI(title="Youtube Scrapper")

origins = ['*']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # Create Text Index on the Field title and description
    db.videos.create_index(
        [('title', TEXT), ('description', TEXT)],
        name="search_title_description",
        weights={
            "title": 100,
            "description": 70
        },
        default_language='english')
    # Create a task to run asynchronously on background to continously scrap
    asyncio.create_task(
        run_scrapper_task(
            REFRESH_INTERVAL, SEARCH_QUERY, API_KEYS
        )
    )

# Redirect to /docs endpoint for swagger documentation


@app.get("/", response_class=RedirectResponse)
async def home():
    return "/dashboard"


# Include video route to show video related apis
app.include_router(videos, prefix="/api", tags=["Videos"])
app.include_router(dashboard, prefix="/dashboard", tags=["Dashboard"])
