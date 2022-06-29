
from pydantic import BaseModel
from datetime import datetime


class VideoModel(BaseModel):
    videoId: str
    title: str
    description: str
    thumbnail: str
    publishTime: datetime

