import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ravenspedia.core import db_helper
from ravenspedia.api_v1 import router as router_v1
from ravenspedia.api_v1.auth.crud import delete_revoked_tokens


# Asynchronous function to delete revoked tokens from the database
async def scheduled_delete_revoked_tokens():
    async with db_helper.session_factory() as session:
        await delete_revoked_tokens(session)


# Wrapper function to run the async token deletion in a synchronous context
def run_scheduled_delete():
    asyncio.run(scheduled_delete_revoked_tokens())


# Define the application lifespan to manage startup and shutdown tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()

    # Add a job to delete revoked tokens every 20 minutes
    scheduler.add_job(
        run_scheduled_delete,  # Function to execute
        "interval",  # Run on a fixed interval
        minutes=20,  # Interval duration
    )

    scheduler.start()  # Start the scheduler on app startup

    yield  # Yield control to the FastAPI app, allowing it to run

    scheduler.shutdown()  # Shut down the scheduler when the app stops


app = FastAPI(
    title="Ravens Pedia API",  # API title for documentation
    lifespan=lifespan,  # Custom lifespan for managing startup/shutdown
)

# List of allowed origins for CORS (shortened using list comprehension)
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
    allow_origins=origins,  # Whitelist of origins allowed to access the API
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
)

app.include_router(router=router_v1)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Module and app instance to run
        host="0.0.0.0",  # Bind to all network interfaces
        port=8000,  # Port to listen on
    )
