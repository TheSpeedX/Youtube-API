from fastapi import APIRouter, Query
from config.database import db
from models.videos import VideoModel
from typing import List

videos = APIRouter()


async def search_videos(query: str, limit: int, offset: int):
    if not query:
        return await db.videos.find().sort(
            "publishTime", -1
        ).skip(offset).to_list(length=limit)
    return await db.videos.find(
        {
            "$text": {
                "$search": query
            }
        },
        {
            "score": {
                "$meta": "textScore"
            }
        }
    ).sort(
        [
            ("score",  {"$meta": "textScore"}),
            ("publishTime", -1)
        ]
    ).skip(offset).to_list(length=limit)


@videos.get('/videos', response_model=List[VideoModel])
async def show_videos(
    query: str = None,
    limit: int = Query(50, ge=1, le=100, description="Page size limit"),
    offset: int = Query(0, ge=0, description="Page offset"),
):
    return await search_videos(query, limit, offset)
