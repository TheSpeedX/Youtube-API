from apiclient.discovery import build
from typing import List, Dict
from itertools import cycle
from datetime import datetime
from config.database import db
from models.videos import VideoModel
import asyncio
import traceback


def extract_info(data: Dict):
    """Extract Necessary info from the API response"""
    thumbnails = data['snippet']['thumbnails']
    # Scan thumbnail via hierachy if high exists else go for medium or low
    thumbnail = thumbnails.get(
        'high',
        thumbnails.get(
            'medium',
            thumbnails.get(
                'default'
            )
        )
    )
    return VideoModel(
        videoId=data['id']['videoId'],
        title=data['snippet']['title'],
        description=data['snippet']['description'],
        thumbnail=thumbnail['url'],
        publishTime=datetime.strptime(
            data['snippet']['publishTime'],
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        channelTitle=data['snippet']['channelTitle']
    )


async def scrap(query: str, youtube):
    # builds the search request
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        order='date',
        maxResults=50,
        publishedAfter='2015-01-01T00:00:00Z'
    )
    res = request.execute()
    print("Started !!!!!")
    print(res["items"])
    for item in res["items"]:
        video = extract_info(item)
        # updates videos if existed else create them
        await db.videos.update_one(
            {"videoId": video.videoId},
            {"$set": video.dict()},
            upsert=True
        )


async def run_scrapper_task(interval: int, query: str, api_keys: List[str]):
    """Starts the scrapper task"""
    # Create a cycle of api keys and rotate it on each request
    api_keys = cycle(api_keys)
    # create youtube request with api key
    youtube = build('youtube', 'v3', developerKey=next(api_keys))
    while True:
        try:
            await asyncio.gather(
                asyncio.sleep(interval),
                scrap(query, youtube),
            )
        except Exception:
            print(traceback.format_exc())
            await asyncio.sleep(interval)
            # recreate youtube request with next api key
            youtube = build('youtube', 'v3', developerKey=next(api_keys))
