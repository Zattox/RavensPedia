from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from core.models import Base, db_helper
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Ravens Pedia API", lifespan=lifespan)
app.include_router(router=router_v1)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
