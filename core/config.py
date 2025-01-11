import os
from dotenv import load_dotenv

from pathlib import Path
from pydantic_settings import BaseSettings

load_dotenv()

# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # The connection string to the database file
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # Database debugging mode
    db_echo: bool = False


class FaceitSettings:
    faceit_base_url = os.getenv("FACEIT_BASE_URL")
    faceit_api_key = os.getenv("FACEIT_API_KEY")


# Init class Settings
settings = Settings()
#
test_settings = Settings(
    db_url=f"sqlite+aiosqlite:///{BASE_DIR}/test_db.sqlite3",
)
# Init class FaceitSettings
faceit_settings = FaceitSettings()
