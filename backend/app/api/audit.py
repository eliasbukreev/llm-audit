from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse

router = APIRouter()


class AuditStartRequest(BaseModel):
    repo_url: str


@router.post("/audit/start")
async def start_audit(req: AuditStartRequest):
    return {"session_id": "placeholder"}


@router.get("/audit/{session_id}/stream")
async def stream_audit(session_id: str):

    async def generator():
        yield b"data: {}\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")


@router.get("/audit/{session_id}/results")
async def get_results(session_id: str):
    return {"files": []}
