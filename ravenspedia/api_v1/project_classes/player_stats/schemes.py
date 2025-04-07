from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class PlayerStatsFilter(BaseModel):
    """
    Pydantic model for filtering player statistics.
    """

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tournament_ids: Optional[List[int]] = None
    detailed: bool = False


class GeneralPlayerStats(BaseModel):
    """
    Pydantic model for a player's general statistics.
    """

    nickname: str
    total_matches: int = Field(0)

    kills: int = Field(0, alias="Kills")
    assists: int = Field(0, alias="Assists")
    deaths: int = Field(0, alias="Deaths")
    adr: float = Field(0.0, alias="ADR")
    kpr: float = Field(0.0, alias="K/R Ratio")
    headshots: int = Field(0, alias="Headshots")
    headshots_rate: float = Field(0.0, alias="Headshots %")

    wins: int = Field(0, alias="Wins")
    win_rate: float = Field(0.0, alias="Wins %")
    kd_ratio: float = Field(0.0, alias="K/D Ratio")


# Mapping of Faceit API stat fields to GeneralPlayerStats fields
GENERAL_STATS_MAPPING = {
    "Result": "wins",
    "Kills": "kills",
    "Deaths": "deaths",
    "Assists": "assists",
    "Headshots": "headshots",
    "ADR": "adr",
    "K/R Ratio": "kpr",
}


class DetailedPlayerStats(BaseModel):
    """
    Pydantic model for a player's detailed statistics, including additional metrics.
    """

    nickname: str
    total_matches: int = Field(0)

    # ------------------General Stats------------------
    kills: int = Field(0, alias="Kills")
    assists: int = Field(0, alias="Assists")
    deaths: int = Field(0, alias="Deaths")
    adr: float = Field(0, alias="ADR")
    headshots_percentage: int = Field(0, alias="Headshots %")

    # -----------------Additional Stats----------------- #

    mvps: int = Field(0, alias="MVPs")
    damage: int = Field(0, alias="Damage")
    headshots: int = Field(0, alias="Headshots")

    kd: float = Field(0, alias="K/D Ratio")
    kpr: float = Field(0, alias="K/R Ratio")

    # --------------------Multikills-------------------- #
    double: int = Field(0, alias="Double Kills")
    triple: int = Field(0, alias="Triple Kills")
    quadro: int = Field(0, alias="Quadro Kills")
    penta: int = Field(0, alias="Penta Kills")

    # ----------------------Clutch---------------------- #
    clutch_kills: int = Field(0, alias="Clutch Kills")
    count_1v1: int = Field(0, alias="1v1Count")
    count_1v2: int = Field(0, alias="1v2Count")
    wins_1v1: int = Field(0, alias="1v1Wins")
    wins_1v2: int = Field(0, alias="1v2Wins")
    match_1v1_win_rate: float = Field(0, alias="Match 1v1 Win Rate")
    match_1v2_win_rate: float = Field(0, alias="Match 1v2 Win Rate")

    # ---------------------Entries--------------------- #
    first_kills: int = Field(0, alias="First Kills")
    entry_count: int = Field(0, alias="Entry Count")
    entry_wins: int = Field(0, alias="Entry Wins")
    match_entry_rate: float = Field(0, alias="Match Entry Rate")
    match_entry_success_rate: float = Field(0, alias="Match Entry Success Rate")

    # ----------------------Sniper---------------------- #
    sniper_kills: int = Field(0, alias="Sniper Kills")
    sniper_kill_rate_per_round: float = Field(0, alias="Sniper Kill Rate per Round")
    sniper_kill_rate_per_match: float = Field(0, alias="Sniper Kill Rate per Match")

    # ------------------Special Kills------------------ #
    pistol_kills: float = Field(0, alias="Pistol Kills")
    knife_kills: int = Field(0, alias="Knife Kills")
    zeus_kills: float = Field(0, alias="Zeus Kills")

    # ---------------------Utility--------------------- #
    utility_count: int = Field(0, alias="Utility Count")
    utility_successes: int = Field(0, alias="Utility Successes")
    utility_enemies: int = Field(0, alias="Utility Enemies")
    utility_damage: int = Field(0, alias="Utility Damage")

    # --------------Average Utility Stats-------------- #
    utility_usage_per_round: float = Field(0, alias="Utility Usage per Round")
    utility_damage_success_rate_per_match: float = Field(
        0, alias="Utility Damage Success Rate per Match"
    )
    utility_successes_rate_per_match: float = Field(
        0, alias="Utility Success Rate per Match"
    )
    utility_damage_per_round_in_a_match: float = Field(
        0, alias="Utility Damage per Round in a Match"
    )

    # ----------------------Flash---------------------- #
    flash_count: int = Field(0, alias="Flash Count")
    enemies_flashed: int = Field(0, alias="Enemies Flashed")
    flash_successes: int = Field(0, alias="Flash Successes")

    # ---------------Average Flash Stats--------------- #
    flashes_per_round_in_a_match: float = Field(0, alias="Flashes per Round in a Match")
    enemies_flashed_per_round_in_a_match: float = Field(
        0, alias="Enemies Flashed per Round in a Match"
    )
    flash_success_rate_per_match: float = Field(0, alias="Flash Success Rate per Match")


# Mapping of Faceit API stat fields to DetailedPlayerStats fields
DETAILED_STATS_MAPPING = {
    "Kills": "kills",
    "Assists": "assists",
    "Deaths": "deaths",
    "Headshots": "headshots",
    "MVPs": "mvps",
    "Damage": "damage",
    "Double Kills": "double",
    "Triple Kills": "triple",
    "Quadro Kills": "quadro",
    "Penta Kills": "penta",
    "Clutch Kills": "clutch_kills",
    "1v1Count": "count_1v1",
    "1v2Count": "count_1v2",
    "1v1Wins": "wins_1v1",
    "1v2Wins": "wins_1v2",
    "First Kills": "first_kills",
    "Entry Count": "entry_count",
    "Entry Wins": "entry_wins",
    "Sniper Kills": "sniper_kills",
    "Pistol Kills": "pistol_kills",
    "Knife Kills": "knife_kills",
    "Zeus Kills": "zeus_kills",
    "Utility Count": "utility_count",
    "Utility Successes": "utility_successes",
    "Utility Enemies": "utility_enemies",
    "Utility Damage": "utility_damage",
    "Flash Count": "flash_count",
    "Enemies Flashed": "enemies_flashed",
    "Flash Successes": "flash_successes",
}
