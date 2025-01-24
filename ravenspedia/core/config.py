import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

# Find the project folder
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # The connection string to the database file
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # Database debugging mode
    db_echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30


class FaceitSettings:
    base_url = "https://open.faceit.com/data/v4"
    api_key = os.getenv("FACEIT_API_KEY")


class DataForTests:
    player1_steam_id = os.getenv("PLAYER1_STEAM_ID")
    player2_steam_id = os.getenv("PLAYER2_STEAM_ID")
    player3_steam_id = os.getenv("PLAYER3_STEAM_ID")
    player4_steam_id = os.getenv("PLAYER4_STEAM_ID")
    player5_steam_id = os.getenv("PLAYER5_STEAM_ID")

    player1_faceit_id = os.getenv("PLAYER1_FACEIT_ID")
    player2_faceit_id = os.getenv("PLAYER2_FACEIT_ID")
    player3_faceit_id = os.getenv("PLAYER3_FACEIT_ID")
    player4_faceit_id = os.getenv("PLAYER4_FACEIT_ID")
    player5_faceit_id = os.getenv("PLAYER5_FACEIT_ID")

    faceit_bo1_match1 = os.getenv("FACEIT_BO1_MATCH1")
    faceit_bo1_match2 = os.getenv("FACEIT_BO1_MATCH2")

    faceit_bo2_match1 = os.getenv("FACEIT_BO2_MATCH1")
    faceit_bo3_match1 = os.getenv("FACEIT_BO3_MATCH1")


# Init class Settings
settings = Settings()
#
test_settings = Settings(
    db_url=f"sqlite+aiosqlite:///{BASE_DIR}/test_db.sqlite3",
)
# Init class FaceitSettings
faceit_settings = FaceitSettings()

data_for_tests = DataForTests()

auth_settings = AuthJWT()
