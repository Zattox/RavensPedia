import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api_v1 import router as router_v1


# Function for configuring the application (creating a database)
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Clean up


app = FastAPI(
    title="Ravens Pedia API",
    lifespan=lifespan,
)
app.include_router(router=router_v1)

# Run the app on port with auto reload
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
