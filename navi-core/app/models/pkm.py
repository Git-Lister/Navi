from pydantic import BaseModel
from typing import Optional, List

class CaptureRequest(BaseModel):
    content: str
    title: Optional[str] = None
    domain: str
    source: Optional[str] = None

class CaptureResponse(BaseModel):
    path: str

class SearchRequest(BaseModel):
    query: str
    k: int = 5

class SearchHit(BaseModel):
    path: str
    score: float

class SearchResponse(BaseModel):
    hits: List[SearchHit]
