from pydantic import BaseModel, Field

from ravenspedia.core.faceit_models.player_stats import PlayerInfo


class TeamStats(BaseModel):
    team: str = Field(..., alias="Team")
    team_win: int = Field(..., alias="Team Win")
    team_headshots: float = Field(..., alias="Team Headshots")

    first_half_score: int = Field(..., alias="First Half Score")
    second_half_score: int = Field(..., alias="Second Half Score")
    overtime_score: int = Field(..., alias="Overtime score")
    final_score: int = Field(..., alias="Final Score")


class TeamInfo(BaseModel):
    faceit_team_id: str = Field(..., alias="team_id")
    premade: bool = Field(..., alias="premade")
    team_stats: TeamStats = Field(..., alias="team_stats")
    players: list[PlayerInfo] = Field(..., alias="players")
