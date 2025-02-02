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

6. Creating Testing Environment variables

To test the application, add the following fields to the `.env`:
- 5 fields of the form `PLAYER1_STEAM_ID` (You can get it from a third-party service, [for example](https://steamid.pro/`), by entering the steam user profile link, you will need to add the SteamID from the site)
- 5 fields of the form `PLAYER1_FACEIT_ID` (You can get it when ordering to [here](https://docs.faceit.com/docs/data-api/data#tag/Players/operation/getPlayer) with an earlier SteamID already found. The Faceit ID will be specified in the player_id field). For example, a `curl` query in PowerShell will look like this:
```powershell
$wget = curl -Headers @{"Accept"="application/json"; "Authorization"="Bearer FACEIT_API_KEY";} -Uri "https://open.faceit.com/data/v4/players?game=cs2&game_player_id=SteamID"
$wget.Content
```
 
- `FACEIT_BO1_MATCH1`, `FACEIT_BO1_MATCH2` (Find two different bo1 format matches on faceit)
- `FACEIT_BO2_MATCH1` (Find any bo2 format match on faceit)
- `FACEIT_BO3_MATCH1` (Find any bo3 format match on faceit)

7. Testing the application
Go to the project folder, then write in the terminal
```bash
poetry run pytest
```
