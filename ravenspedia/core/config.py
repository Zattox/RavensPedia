import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()  # Load environment variables from a .env file

# Determine the base directory of the project (two levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent


# Defines the main settings class for the application
class Settings(BaseSettings):
    # Database connection string, defaults to a SQLite database in the project directory
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"

    # Flag to enable/disable SQL statement logging for debugging, defaults to False
    db_echo: bool = False


# Defines JWT authentication settings as a Pydantic model
class AuthJWT(BaseModel):
    # Path to the private key for JWT signing, defaults to a file in the certs directory
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"

    # Path to the public key for JWT verification, defaults to a file in the certs directory
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"

    # Algorithm used for JWT signing, defaults to RS256 (RSA with SHA-256)
    algorithm: str = "RS256"

    # Expiration time for access tokens in minutes, defaults to 15
    access_token_expire_minutes: int = 15

    # Expiration time for refresh tokens in days, defaults to 14
    refresh_token_expire_days: int = 14

    # Field name used to indicate token type in the payload
    TOKEN_TYPE_FIELD: str = "token_type"

    # Value for access token type
    ACCESS_TOKEN_TYPE: str = "access"

    # Value for refresh token type
    REFRESH_TOKEN_TYPE: str = "refresh"


# Defines settings for interacting with the FACEIT API
class FaceitSettings:
    # Base URL for the FACEIT API
    base_url = "https://open.faceit.com/data/v4"

    # API key for FACEIT, loaded from environment variables
    api_key = os.getenv("FACEIT_API_KEY")


# Defines test data for use in automated tests
class DataForTests:
    # Steam IDs for test players, loaded from environment variables
    player1_steam_id = os.getenv("PLAYER1_STEAM_ID")
    player2_steam_id = os.getenv("PLAYER2_STEAM_ID")
    player3_steam_id = os.getenv("PLAYER3_STEAM_ID")
    player4_steam_id = os.getenv("PLAYER4_STEAM_ID")
    player5_steam_id = os.getenv("PLAYER5_STEAM_ID")

    # FACEIT IDs for test players, loaded from environment variables
    player1_faceit_id = os.getenv("PLAYER1_FACEIT_ID")
    player2_faceit_id = os.getenv("PLAYER2_FACEIT_ID")
    player3_faceit_id = os.getenv("PLAYER3_FACEIT_ID")
    player4_faceit_id = os.getenv("PLAYER4_FACEIT_ID")
    player5_faceit_id = os.getenv("PLAYER5_FACEIT_ID")

    # FACEIT match IDs for best-of-1 matches, loaded from environment variables
    faceit_bo1_match1 = os.getenv("FACEIT_BO1_MATCH1")
    faceit_bo1_match2 = os.getenv("FACEIT_BO1_MATCH2")

    # FACEIT match IDs for best-of-2 and best-of-3 matches, loaded from environment variables
    faceit_bo2_match1 = os.getenv("FACEIT_BO2_MATCH1")
    faceit_bo3_match1 = os.getenv("FACEIT_BO3_MATCH1")


# Initialize the main settings instance
settings = Settings()

# Initialize the test settings instance with a different database URL
test_settings = Settings(
    db_url=f"sqlite+aiosqlite:///{BASE_DIR}/test_db.sqlite3",  # Use a separate SQLite database for tests
)

# Initialize the FACEIT settings instance
faceit_settings = FaceitSettings()

# Initialize the test data instance
data_for_tests = DataForTests()

# Initialize the JWT authentication settings instance
auth_settings = AuthJWT()
