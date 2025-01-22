from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core import Base

if TYPE_CHECKING:
    from .table_team import TableTeam
    from .table_tournament import TableTournament
    from .table_match_stats import TableMatchStats


class TablePlayer(Base):
    __tablename__ = "players"

    # The player's game name
    nickname: Mapped[str] = mapped_column(
        String(12),
        unique=True,
    )
    steam_id: Mapped[str] = mapped_column(unique=True)
    # The player's real name
    name: Mapped[str | None] = mapped_column(String(15))
    # The player's real surname
    surname: Mapped[str | None] = mapped_column(String(30))

    faceit_id: Mapped[str | None] = mapped_column(unique=True)

    # The ID of the player's current team
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    team: Mapped["TableTeam"] = relationship(back_populates="players")

    # Статистика игрока в матчах
    stats: Mapped[list["TableMatchStats"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )

    # The IDs of the tournaments the team participated in
    tournaments: Mapped[list["TableTournament"]] = relationship(
        secondary="player_tournament_association",
        back_populates="players",
        cascade="save-update, merge",
    )
