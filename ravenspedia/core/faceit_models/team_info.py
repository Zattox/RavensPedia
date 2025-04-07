from pydantic import BaseModel, Field

from .player_stats import PlayerInfo


# Defines the TeamStats model for team performance statistics in a match
class TeamStats(BaseModel):
    # Name or ID of the team, required field with alias "Team"
    team: str = Field(..., alias="Team")

    # Indicator of team win (1 for win, 0 for loss), required field with alias "Team Win"
    team_win: int = Field(..., alias="Team Win")

    # Percentage of headshots by the team, required field with alias "Team Headshots"
    team_headshots: float = Field(..., alias="Team Headshots")

    # Team's score in the first half, required field with alias "First Half Score"
    first_half_score: int = Field(..., alias="First Half Score")

    # Team's score in the second half, required field with alias "Second Half Score"
    second_half_score: int = Field(..., alias="Second Half Score")

    # Team's score in overtime, required field with alias "Overtime score"
    overtime_score: int = Field(..., alias="Overtime score")

    # Team's final score, required field with alias "Final Score"
    final_score: int = Field(..., alias="Final Score")


# Defines the TeamInfo model for detailed team information in a match
class TeamInfo(BaseModel):
    # FACEIT team ID, required field with alias "team_id"
    faceit_team_id: str = Field(..., alias="team_id")

    # Indicates if the team is premade (pre-assembled), required field with alias "premade"
    premade: bool = Field(..., alias="premade")

    # Nested TeamStats object containing team statistics, required field with alias "team_stats"
    team_stats: TeamStats = Field(..., alias="team_stats")

    # List of players in the team, required field with alias "players"
    players: list[PlayerInfo] = Field(..., alias="players")
