from fastapi import APIRouter
from app.models.pkm import (
    CaptureRequest,
    CaptureResponse,
    SearchRequest,
    SearchResponse,
    SearchHit,
)
from app.core.pkm_capture import capture_to_markdown
from app.core.pkm_search import PKMSearchIndex

router = APIRouter()
index = PKMSearchIndex()

@router.post("/capture", response_model=CaptureResponse)
async def capture(req: CaptureRequest):
    path = capture_to_markdown(req)
    return CaptureResponse(path=str(path))

@router.post("/reindex")
async def reindex():
    index.build_index()
    return {"status": "ok", "docs": len(index.docs)}

@router.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    index.load_index()
    hits = index.search(req.query, k=req.k)
    return SearchResponse(
        hits=[SearchHit(path=h["path"], score=h["score"]) for h in hits]
    )
