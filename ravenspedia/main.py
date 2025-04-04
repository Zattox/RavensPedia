import asyncio
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ravenspedia.api_v1 import router as router_v1
from ravenspedia.api_v1.auth.crud import mark_expired_and_delete_revoked_tokens
from ravenspedia.core import db_helper

async def scheduled_mark_expired_and_delete_revoked_tokens():
    async with db_helper.session_factory() as session:
        await mark_expired_and_delete_revoked_tokens(session)

def run_scheduled_task():
    asyncio.run(scheduled_mark_expired_and_delete_revoked_tokens())

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_scheduled_task,
        "interval",
        minutes=1,
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
        port=8000,
        ssl_keyfile="ravenspedia/certs/key.pem",
        ssl_certfile="ravenspedia/certs/cert.pem",
    )