from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import HOST, PORT
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="llm-server-dib", lifespan=lifespan)

from app.api import health, audit  # noqa: E402

app.include_router(health.router)
app.include_router(audit.router)
