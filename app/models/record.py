from typing import Optional
from pydantic import BaseModel

class ArticleRecord(BaseModel):
    id: int
    title: str
    user_id: int
    url: str
    cover_url: str
    aspect_ratio: float
    summary: Optional[str] = None
    summary_short: Optional[str] = None

class ChunkRecord(BaseModel):
    id: int
    article_id: int
    content: str
    url: str