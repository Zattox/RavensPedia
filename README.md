<!--Installation-->

## Installation

1. Cloning the repository

```bash
git clone https://github.com/Zattox/RavensPedia.git
```

2. Installation of poetry

The installation process is described [here](https://www.jetbrains.com/help/pycharm/poetry.html#install-poetry)

3. Installing dependencies

Go to the project folder, then write in the terminal

```bash
poetry install
```

4. Creating Environment variables

Create a `.env` file in the root folder of the project and enter your environment variable values: `FACEIT_API_KEY`

5. Getting FACEIT_API_KEY

Getting the API_KEY is described [here](https://developers.faceit.com/docs/auth/api-keys)

<!--Database Setup-->

## Database Setup

1. Install SQLite3 (if not installed):

```bash
sudo apt-get install sqlite3  # Linux
brew install sqlite           # macOS
```

2. Create databases

```bash
cd ravenspedia
sqlite3 db.sqlite3 ".exit"
sqlite3 test_db.sqlite3 ".exit"
```

3. Run migrations

```bash
poetry run alembic upgrade head
```

<!--SSL Certificates Setup-->

## SSL Certificates Setup

1. Create certs directory:

```bash
mkdir -p ./ravenspedia/certs
cd ./ravenspedia/certs
```

2. Generate JWT keys:

```bash
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -pubout -out jwt-public.pem
```

3. Generate HTTPS certificates:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -days 365 \
    -keyout key.pem -out cert.pem \
    -subj "/C=RU/ST=Moscow-State/L=Moscow/O=HSE/OU=CourseProject/CN=localhost"
chmod 600 *.pem
```

<!--Launch Instructions-->

## Launch Instructions

### Option 1: Local Development

1. Configure the application by updating main.py with:

```python
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8000,
        ssl_keyfile="./certs/key.pem",
        ssl_certfile="./certs/cert.pem",
    )
```

2. Start the development server using either:

- Command line:
  ```bash
  cd ravenspedia
  poetry run python main.py
  ```
- Through your IDE: Run main.py directly from PyCharm/VSCode

### Option 2: Production Deployment

Get access to the ongoing project at:
https://ravenspedia.duckdns.org/

<!--Testing-->

## Testing

1. Creating Testing Environment variables

To test the application, add the following fields to the `.env`:

- 5 fields of the form `PLAYER1_STEAM_ID` (You can get it from a third-party
  service, [for example](https://steamid.pro/`), by entering the steam user profile link, you will need to add the
  SteamID from the site)
- 5 fields of the form `PLAYER1_FACEIT_ID` (You can get it when ordering
  to [here](https://docs.faceit.com/docs/data-api/data#tag/Players/operation/getPlayer) with an earlier SteamID already
  found. The Faceit ID will be specified in the player_id field). For example, a `curl` query in PowerShell will look
  like this:

```powershell
$wget = curl -Headers @{"Accept"="application/json"; "Authorization"="Bearer FACEIT_API_KEY";} -Uri "https://open.faceit.com/data/v4/players?game=cs2&game_player_id=SteamID"
$wget.Content
```

- `FACEIT_BO1_MATCH1`, `FACEIT_BO1_MATCH2` (Find two different bo1 format matches on faceit)
- `FACEIT_BO2_MATCH1` (Find any bo2 format match on faceit)
- `FACEIT_BO3_MATCH1` (Find any bo3 format match on faceit)

2. Testing the application
   Go to the project folder, then write in the terminal

```bash
poetry run pytest
```

<!--Test Coverage Setup and Execution-->

## Test Coverage Setup and Execution

1. Install coverage.py

```bash
pip install coverage
```

2. Run tests with coverage

```bash
coverage run -m pytest
coverage report
```

3. Generate HTML report (optional)

```bash
coverage html
```

- Then open htmlcov/index.html in your browser.

4. Configuration (optional)

- Create .coveragerc for custom settings:

```
[run]
omit =
    */tests/*
    */__init__.py
    */ravenspedia/core/*
    */ravenspedia/main.py
```
