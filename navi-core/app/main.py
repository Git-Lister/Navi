from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import chat, pkm  # <- pkm must be imported

app = FastAPI(title="NaviG8 Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:1420"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
app.include_router(pkm.router, prefix="/v1/pkm", tags=["pkm"])  # <- this line

@app.get("/health")
async def health():
    return {"status": "ok", "component": "NaviG8 Core"}
