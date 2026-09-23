import asyncio
import json
import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.config import settings
from app.database import create_session, create_step, get_session, update_session, update_step
from app.graph.state_graph import get_graph
from app.tools import git_tools

router = APIRouter()
event_bus: dict[str, asyncio.Queue] = {}
graph = get_graph()


class AuditStartRequest(BaseModel):
    repo_url: str


async def run_audit(session_id: str, repo_url: str):
    try:
        await event_bus[session_id].put({
            "step": "setup",
            "status": "running",
            "log": "Cloning repo...",
        })

        repo_path = await asyncio.to_thread(git_tools.git_clone, repo_url)
        if repo_path.startswith("ERROR:"):
            await event_bus[session_id].put({
                "step": "setup",
                "status": "error",
                "log": repo_path,
            })
            update_step(session_id, "setup", "error", error=repo_path)
            update_session(session_id, status="error", error_msg=repo_path)
            await event_bus[session_id].put({"step": "complete", "status": "error"})
            return

        await event_bus[session_id].put({"step": "setup", "status": "done", "repo_path": repo_path})
        update_step(session_id, "setup", "done", result_path=repo_path)

        await event_bus[session_id].put({"step": "5.1", "status": "running"})
        create_step(session_id, "5.1", "Анализ текущего состояния")
        update_step(session_id, "5.1", "running")

        result = await graph.ainvoke({
            "session_id": session_id,
            "repo_path": repo_path,
            "messages": [],
        })

        await event_bus[session_id].put({
            "step": "5.1",
            "status": "done",
            "result": result.get("result"),
            "error": result.get("error"),
        })
        update_step(session_id, "5.1", "done", result_path=result.get("result"))
        update_session(session_id, status="done")

        await event_bus[session_id].put({"step": "complete", "status": "done"})
    except Exception as e:
        await event_bus[session_id].put({"step": "error", "status": "error", "log": str(e)})
        update_session(session_id, status="error", error_msg=str(e))


@router.post("/audit/start")
async def start_audit(req: AuditStartRequest):
    session_id = create_session(req.repo_url)
    create_step(session_id, "setup", "Клонирование репозитория")
    create_step(session_id, "5.1", "Анализ текущего состояния")
    event_bus[session_id] = asyncio.Queue()
    asyncio.create_task(run_audit(session_id, req.repo_url))
    return {"session_id": session_id}


@router.get("/audit/{session_id}/stream")
async def stream_audit(session_id: str):
    if session_id not in event_bus:
        raise HTTPException(status_code=404, detail="Session not found")

    queue = event_bus[session_id]

    async def generator():
        while True:
            event = await queue.get()
            yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
            if event.get("step") == "complete" or event.get("step") == "error":
                break

    return StreamingResponse(generator(), media_type="text/event-stream")


@router.get("/audit/{session_id}/results")
async def get_results(session_id: str):
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    files = []
    results_dir = str(settings.results_dir)
    if os.path.isdir(results_dir):
        for root, _dirs, filenames in os.walk(results_dir):
            for f in filenames:
                if f.endswith(".md"):
                    files.append(os.path.join(root, f))

    return {"files": files}
