from typing import Optional, List
from pydantic import BaseModel, ConfigDict
import importlib

from schemes.team.scheme import Team

class TournamentBase(BaseModel):
    name: str
    prize: str
    description: Optional[str] = None
    matches: Optional[List[dict]] = None
    teams: Optional[List[Team]] = None

class TournamentCreate(TournamentBase):
    pass

class TournamentUpdate(TournamentBase):
    pass

class TournamentUpdatePartial(TournamentCreate):
    pass

class Tournament(TournamentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = ...

    def add_team(self, team_data):
        Team = importlib.import_module('schemes.team.scheme').Player
        team = Team(**team_data)
        self.teams.append(team)

    def add_match(self, match_data):
        Match = importlib.import_module('schemes.match.scheme').Match
        match = Match(**match_data)
        self.matches.append(match)