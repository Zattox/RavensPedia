from sqlalchemy.orm import Mapped


class TeamStats:
    team: Mapped[str]
    team_win: Mapped[int]
    team_headshots: Mapped[float]

    first_half_score: Mapped[int]
    second_half_score: Mapped[int]
    overtime_score: Mapped[int]
    final_score: Mapped[int]
