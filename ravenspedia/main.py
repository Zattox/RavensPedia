import asyncio
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

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
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_scheduled_delete,  # используем синхронную обертку
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

app.include_router(router=router_v1)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
