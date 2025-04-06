from typing import Union

from pydantic import BaseModel, Field


class PlayerStats(BaseModel):
    nickname: str
    round_of_match: int
    match_id: int
    map: str
    result: int = Field(..., alias="Result")  # Did the player win this match?

    # ------------------General Stats------------------
    kills: int = Field(..., alias="Kills")  # Number of kills per match
    assists: int = Field(..., alias="Assists")  # Number of assists per match
    deaths: int = Field(..., alias="Deaths")  # Number of deaths per match
    adr: float = Field(..., alias="ADR")  # Average damage per round
    headshots_percentage: int = Field(
        ..., alias="Headshots %"
    )  # The percentage of kills per head

    # -----------------Additional Stats----------------- #
    mvps: Union[int, None] = Field(
        None, alias="MVPs"
    )  # Number of awards for the "Most Valuable Player" per match
    damage: Union[int, None] = Field(
        None, alias="Damage"
    )  # Total amount of damage done per match
    headshots: Union[int, None] = Field(
        None, alias="Headshots"
    )  # Number of headshots per match

    kd: Union[float, None] = Field(
        None, alias="K/D Ratio"
    )  # Kills divided by deaths (K/D)
    kpr: Union[float, None] = Field(
        None, alias="K/R Ratio"
    )  # Kills divided by rounds (KPR)

    # --------------------Multikills-------------------- #
    double: Union[int, None] = Field(
        None, alias="Double Kills"
    )  # The number of rounds where exactly 2 kills were made
    triple: Union[int, None] = Field(
        None, alias="Triple Kills"
    )  # The number of rounds where exactly 3 kills were made
    quadro: Union[int, None] = Field(
        None, alias="Quadro Kills"
    )  # The number of rounds where exactly 4 kills were made
    penta: Union[int, None] = Field(
        None, alias="Penta Kills"
    )  # The number of rounds where exactly 5 kills were made

    # ----------------------Clutch---------------------- #
    clutch_kills: Union[int, None] = Field(
        None, alias="Clutch Kills"
    )  # The number of clutch kills
    count_1v1: Union[int, None] = Field(
        None, alias="1v1Count"
    )  # Number of clutch situations 1vs1
    count_1v2: Union[int, None] = Field(
        None, alias="1v2Count"
    )  # Number of clutch situations 1vs2
    wins_1v1: Union[int, None] = Field(
        None, alias="1v1Wins"
    )  # Number of wins in a 1vs1 clutch situation
    wins_1v2: Union[int, None] = Field(
        None, alias="1v2Wins"
    )  # Number of wins in a 1vs2 clutch situation
    match_1v1_win_rate: Union[float, None] = Field(
        None, alias="Match 1v1 Win Rate"
    )  # Win rate in 1vs1
    match_1v2_win_rate: Union[float, None] = Field(
        None, alias="Match 1v2 Win Rate"
    )  # Win rate in 1vs2

    # ---------------------Entries--------------------- #
    first_kills: Union[int, None] = Field(
        None, alias="First Kills"
    )  # The number of first kill
    entry_count: Union[int, None] = Field(
        None, alias="Entry Count"
    )  # The number of first duels
    entry_wins: Union[int, None] = Field(
        None, alias="Entry Wins"
    )  # The number of wins in the first duels
    match_entry_rate: Union[float, None] = Field(
        None, alias="Match Entry Rate"
    )  # The number of participants in the first duels
    match_entry_success_rate: Union[float, None] = Field(
        None, alias="Match Entry Success Rate"
    )  # Win rate in the first duels

    # ----------------------Sniper---------------------- #
    sniper_kills: Union[int, None] = Field(
        None, alias="Sniper Kills"
    )  # Number of sniper kills
    sniper_kill_rate_per_round: Union[float, None] = Field(
        None, alias="Sniper Kill Rate per Round"
    )  # Number of sniper kills per round
    sniper_kill_rate_per_match: Union[float, None] = Field(
        None, alias="Sniper Kill Rate per Match"
    )  # ???

    # ------------------Special Kills------------------ #
    pistol_kills: Union[float, None] = Field(
        None, alias="Pistol Kills"
    )  # Number of pistol kills
    knife_kills: Union[int, None] = Field(
        None, alias="Knife Kills"
    )  # Number of knife kills
    zeus_kills: Union[float, None] = Field(
        None, alias="Zeus Kills"
    )  # Number of zeus kills

    # ---------------------Utility--------------------- #
    utility_count: Union[int, None] = Field(
        None, alias="Utility Count"
    )  # Number of utility
    utility_successes: Union[int, None] = Field(
        None, alias="Utility Successes"
    )  # Number of helpful utility
    utility_enemies: Union[int, None] = Field(None, alias="Utility Enemies")  # ???
    utility_damage: Union[int, None] = Field(
        None, alias="Utility Damage"
    )  # Utility damage per match

    # --------------Average Utility Stats-------------- #
    utility_usage_per_round: Union[float, None] = Field(
        None, alias="Utility Usage per Round"
    )
    utility_damage_success_rate_per_match: Union[float, None] = Field(
        None, alias="Utility Damage Success Rate per Match"
    )
    utility_successes_rate_per_match: Union[float, None] = Field(
        None, alias="Utility Success Rate per Match"
    )
    utility_damage_per_round_in_a_match: Union[float, None] = Field(
        None, alias="Utility Damage per Round in a Match"
    )

    # ----------------------Flash---------------------- #
    flash_count: Union[int, None] = Field(None, alias="Flash Count")  # Number of flash
    enemies_flashed: Union[int, None] = Field(
        None, alias="Enemies Flashed"
    )  # The number of enemies blinded by the flash
    flash_successes: Union[int, None] = Field(
        None, alias="Flash Successes"
    )  # Number of helpful flash

    # ---------------Average Flash Stats--------------- #
    flashes_per_round_in_a_match: Union[float, None] = Field(
        None, alias="Flashes per Round in a Match"
    )
    enemies_flashed_per_round_in_a_match: Union[float, None] = Field(
        None, alias="Enemies Flashed per Round in a Match"
    )
    flash_success_rate_per_match: Union[float, None] = Field(
        None, alias="Flash Success Rate per Match"
    )


class PlayerInfo(BaseModel):
    faceit_player_id: str = Field(..., alias="player_id")
    faceit_nickname: str = Field(..., alias="nickname")
    player_stats: PlayerStats = Field(..., alias="player_stats")
