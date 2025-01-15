from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ravenspedia.core.base import Base

if TYPE_CHECKING:
    from ravenspedia.core import TablePlayer, TableMatch


class TablePlayerStats(Base):
    __tablename__ = "player_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"))
    player: Mapped["TablePlayer"] = relationship(back_populates="stats")
    match: Mapped["TableMatch"] = relationship(back_populates="stats")

    # ------------------General Stats------------------
    round: Mapped[int] = mapped_column()
    nickname: Mapped[str] = mapped_column()
    kills: Mapped[int] = mapped_column()  # Number of kills per match
    assists: Mapped[int] = mapped_column()  # Number of assists per match
    deaths: Mapped[int] = mapped_column()  # Number of deaths per match
    headshots_percentage: Mapped[int] = (
        mapped_column()
    )  # The percentage of kills per head
    adr: Mapped[float] = mapped_column()  # Average damage per round
    result: Mapped[int] = mapped_column()  # Did the player win this match?

    # -----------------Additional Stats----------------- #
    mvps: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of awards for the "Most Valuable Player" per match
    damage: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Total amount of damage done per match
    headshots: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of headshots per match
    kd: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Kills divided by deaths (K/D)
    kpr: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Kills divided by rounds (KPR)

    # --------------------Multikills-------------------- #
    double: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of rounds where exactly 2 kills were made
    triple: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of rounds where exactly 3 kills were made
    quadro: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of rounds where exactly 4 kills were made
    penta: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of rounds where exactly 5 kills were made

    # ----------------------Clutch---------------------- #
    clutch_kills: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of clutch kills
    count_1v1: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of clutch situations 1vs1
    count_1v2: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of clutch situations 1vs2
    wins_1v1: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of wins in a 1vs1 clutch situation
    wins_1v2: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of wins in a 1vs2 clutch situation
    match_1v1_win_rate: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Win rate in 1vs1
    match_1v2_win_rate: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Win rate in 1vs2

    # ---------------------Entries--------------------- #
    first_kills: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of first kill
    entry_count: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of first duels
    entry_wins: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of wins in the first duels
    match_entry_rate: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of participants in the first duels
    match_entry_success_rate: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Win rate in the first duels

    # ----------------------Sniper---------------------- #
    sniper_kills: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of sniper kills
    sniper_kill_rate_per_round: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of sniper kills per round
    sniper_kill_rate_per_match: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # ???

    # ------------------Special Kills------------------ #
    pistol_kills: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of pistol kills
    knife_kills: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of knife kills
    zeus_kills: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of zeus kills

    # ---------------------Utility--------------------- #
    utility_count: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of utility
    utility_successes: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of helpful utility
    utility_enemies: Mapped[int | None] = mapped_column()  # ???
    utility_damage: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Utility damage per match

    # --------------Average Utility Stats-------------- #
    utility_usage_per_round: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )
    utility_damage_success_rate_per_match: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )
    utility_successes_rate_per_match: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )
    utility_damage_per_round_in_a_match: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )

    # ----------------------Flash---------------------- #
    flash_count: Mapped[int | None] = mapped_column()  # Number of flash
    enemies_flashed: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # The number of enemies blinded by the flash
    flash_successes: Mapped[int | None] = mapped_column(
        default=None,
        server_default=None,
    )  # Number of helpful flash

    # ---------------Average Flash Stats--------------- #
    flashes_per_round_in_a_match: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )
    enemies_flashed_per_round_in_a_match: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )
    flash_success_rate_per_match: Mapped[float | None] = mapped_column(
        default=None,
        server_default=None,
    )
