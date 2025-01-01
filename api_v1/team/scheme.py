from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import importlib


class TeamBase(BaseModel):
    name: str = ...
    description: Optional[str] = None
    matches: Optional[List[dict]] = None
    players: Optional[List[dict]] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    pass


class TeamUpdatePartial(TeamCreate):
    pass


class Team(TeamBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = ...

    def add_player(self, player_data):
        Player = importlib.import_module("api_v1.player.schema").Player
        player = Player(**player_data)
        self.players.append(player)

    def add_match(self, match_data):
        Match = importlib.import_module("api_v1.match.schema").Match
        match = Match(**match_data)
        self.matches.append(match)
