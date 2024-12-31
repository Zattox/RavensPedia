from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import importlib

class TeamBase(BaseModel):
    name: str
    description: str
    matches: List[dict]
    players: List[dict]

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    pass

class TeamUpdatePartial(TeamCreate):
    name: Optional[str] = None
    description: Optional[str] = None
    matches: Optional[List[dict]] = None
    players: Optional[List[dict]] = None

class Team(TeamBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

    def add_player(self, player_data):
        Player = importlib.import_module('schemes.player.schema').Player
        player = Player(**player_data)
        self.players.append(player)

    def add_match(self, match_data):
        Match = importlib.import_module('schemes.match.schema').Match
        match = Match(**match_data)
        self.matches.append(match)