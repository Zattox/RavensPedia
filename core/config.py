from pathlib import Path
from pydantic_settings import BaseSettings

# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # The connection string to the database file
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # Database debugging mode
    db_echo: bool = False


# Init class Settings
settings = Settings()
