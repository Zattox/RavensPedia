import asyncio
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ravenspedia.api_v1 import router as router_v1
from ravenspedia.api_v1.auth.crud import delete_revoked_tokens
from ravenspedia.core import db_helper

async def scheduled_delete_revoked_tokens():
    async with db_helper.session_factory() as session:
        await delete_revoked_tokens(session)


def run_scheduled_delete():
    asyncio.run(scheduled_delete_revoked_tokens())

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_scheduled_delete,
        "interval",
        minutes=20,
    )
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(
    title="Ravens Pedia API",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://localhost:5173",
    "https://localhost:5174",
    "https://127.0.0.1:5173",
    "https://127.0.0.1:5174",
    "http://90.156.158.26/",
    "https://90.156.158.26/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
)
app.include_router(router=router_v1)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )