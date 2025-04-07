from typing import Union

from pydantic import BaseModel, Field


# Defines the PlayerStats model for detailed player statistics in a match
class PlayerStats(BaseModel):
    # Player's nickname, required field
    nickname: str

    # Round number within the match, required field
    round_of_match: int

    # Unique match ID, required field
    match_id: int

    # Name of the map played (e.g., "Inferno"), required field
    map: str

    # Result of the match for the player (1 for win, 0 for loss), required field with alias "Result"
    result: int = Field(..., alias="Result")  # Did the player win this match?

    # ------------------General Stats------------------ #

    # Number of kills by the player in the match, required field with alias "Kills"
    kills: int = Field(..., alias="Kills")

    # Number of assists by the player in the match, required field with alias "Assists"
    assists: int = Field(..., alias="Assists")

    # Number of deaths of the player in the match, required field with alias "Deaths"
    deaths: int = Field(..., alias="Deaths")

    # Average damage per round (ADR), required field with alias "ADR"
    adr: float = Field(..., alias="ADR")

    # Percentage of kills that were headshots, required field with alias "Headshots %"
    headshots_percentage: int = Field(..., alias="Headshots %")

    # -----------------Additional Stats----------------- #

    # Number of MVP awards, optional field with alias "MVPs"
    mvps: Union[int, None] = Field(None, alias="MVPs")

    # Total damage dealt in the match, optional field with alias "Damage"
    damage: Union[int, None] = Field(None, alias="Damage")

    # Number of headshots, optional field with alias "Headshots"
    headshots: Union[int, None] = Field(None, alias="Headshots")

    # Kill/Death ratio (K/D), optional field with alias "K/D Ratio"
    kd: Union[float, None] = Field(None, alias="K/D Ratio")

    # Kills per round (KPR), optional field with alias "K/R Ratio"
    kpr: Union[float, None] = Field(None, alias="K/R Ratio")

    # --------------------Multikills-------------------- #

    # Number of double kills (2 kills in a round), optional field with alias "Double Kills"
    double: Union[int, None] = Field(None, alias="Double Kills")

    # Number of triple kills (3 kills in a round), optional field with alias "Triple Kills"
    triple: Union[int, None] = Field(None, alias="Triple Kills")

    # Number of quadro kills (4 kills in a round), optional field with alias "Quadro Kills"
    quadro: Union[int, None] = Field(None, alias="Quadro Kills")

    # Number of penta kills (5 kills in a round), optional field with alias "Penta Kills"
    penta: Union[int, None] = Field(None, alias="Penta Kills")

    # ----------------------Clutch---------------------- #

    # Number of clutch kills, optional field with alias "Clutch Kills"
    clutch_kills: Union[int, None] = Field(None, alias="Clutch Kills")

    # Number of 1v1 clutch situations, optional field with alias "1v1Count"
    count_1v1: Union[int, None] = Field(None, alias="1v1Count")

    # Number of 1v2 clutch situations, optional field with alias "1v2Count"
    count_1v2: Union[int, None] = Field(None, alias="1v2Count")

    # Number of 1v1 clutch wins, optional field with alias "1v1Wins"
    wins_1v1: Union[int, None] = Field(None, alias="1v1Wins")

    # Number of 1v2 clutch wins, optional field with alias "1v2Wins"
    wins_1v2: Union[int, None] = Field(None, alias="1v2Wins")

    # Win rate in 1v1 clutch situations, optional field with alias "Match 1v1 Win Rate"
    match_1v1_win_rate: Union[float, None] = Field(None, alias="Match 1v1 Win Rate")

    # Win rate in 1v2 clutch situations, optional field with alias "Match 1v2 Win Rate"
    match_1v2_win_rate: Union[float, None] = Field(None, alias="Match 1v2 Win Rate")

    # ---------------------Entries--------------------- #

    # Number of first kills in rounds, optional field with alias "First Kills"
    first_kills: Union[int, None] = Field(None, alias="First Kills")

    # Number of entry duels (first engagements), optional field with alias "Entry Count"
    entry_count: Union[int, None] = Field(None, alias="Entry Count")

    # Number of entry duel wins, optional field with alias "Entry Wins"
    entry_wins: Union[int, None] = Field(None, alias="Entry Wins")

    # Rate of participation in entry duels, optional field with alias "Match Entry Rate"
    match_entry_rate: Union[float, None] = Field(None, alias="Match Entry Rate")

    # Success rate in entry duels, optional field with alias "Match Entry Success Rate"
    match_entry_success_rate: Union[float, None] = Field(
        None,
        alias="Match Entry Success Rate",
    )

    # ----------------------Sniper---------------------- #

    # Number of sniper kills, optional field with alias "Sniper Kills"
    sniper_kills: Union[int, None] = Field(None, alias="Sniper Kills")

    # Sniper kills per round, optional field with alias "Sniper Kill Rate per Round"
    sniper_kill_rate_per_round: Union[float, None] = Field(
        None,
        alias="Sniper Kill Rate per Round",
    )

    # Sniper kill rate per match, optional field with alias "Sniper Kill Rate per Match"
    sniper_kill_rate_per_match: Union[float, None] = Field(
        None,
        alias="Sniper Kill Rate per Match",
    )

    # ------------------Special Kills------------------ #

    # Number of pistol kills, optional field with alias "Pistol Kills"
    pistol_kills: Union[float, None] = Field(None, alias="Pistol Kills")

    # Number of knife kills, optional field with alias "Knife Kills"
    knife_kills: Union[int, None] = Field(None, alias="Knife Kills")

    # Number of Zeus (taser) kills, optional field with alias "Zeus Kills"
    zeus_kills: Union[float, None] = Field(None, alias="Zeus Kills")

    # ---------------------Utility--------------------- #

    # Number of utility items used (e.g., grenades), optional field with alias "Utility Count"
    utility_count: Union[int, None] = Field(None, alias="Utility Count")

    # Number of successful utility uses, optional field with alias "Utility Successes"
    utility_successes: Union[int, None] = Field(None, alias="Utility Successes")

    # Number of enemies affected by utility, optional field with alias "Utility Enemies"
    utility_enemies: Union[int, None] = Field(None, alias="Utility Enemies")

    # Total utility damage dealt, optional field with alias "Utility Damage"
    utility_damage: Union[int, None] = Field(None, alias="Utility Damage")

    # --------------Average Utility Stats-------------- #

    # Utility usage per round, optional field with alias "Utility Usage per Round"
    utility_usage_per_round: Union[float, None] = Field(
        None,
        alias="Utility Usage per Round",
    )

    # Utility damage success rate per match, optional field with alias "Utility Damage Success Rate per Match"
    utility_damage_success_rate_per_match: Union[float, None] = Field(
        None,
        alias="Utility Damage Success Rate per Match",
    )

    # Utility success rate per match, optional field with alias "Utility Success Rate per Match"
    utility_successes_rate_per_match: Union[float, None] = Field(
        None,
        alias="Utility Success Rate per Match",
    )

    # Utility damage per round, optional field with alias "Utility Damage per Round in a Match"
    utility_damage_per_round_in_a_match: Union[float, None] = Field(
        None,
        alias="Utility Damage per Round in a Match",
    )

    # ----------------------Flash---------------------- #

    # Number of flashbangs used, optional field with alias "Flash Count"
    flash_count: Union[int, None] = Field(None, alias="Flash Count")

    # Number of enemies blinded by flashbangs, optional field with alias "Enemies Flashed"
    enemies_flashed: Union[int, None] = Field(None, alias="Enemies Flashed")

    # Number of successful flashbang uses, optional field with alias "Flash Successes"
    flash_successes: Union[int, None] = Field(None, alias="Flash Successes")

    # ---------------Average Flash Stats--------------- #

    # Flashbangs used per round, optional field with alias "Flashes per Round in a Match"
    flashes_per_round_in_a_match: Union[float, None] = Field(
        None,
        alias="Flashes per Round in a Match",
    )

    # Enemies flashed per round, optional field with alias "Enemies Flashed per Round in a Match"
    enemies_flashed_per_round_in_a_match: Union[float, None] = Field(
        None,
        alias="Enemies Flashed per Round in a Match",
    )

    # Flash success rate per match, optional field with alias "Flash Success Rate per Match"
    flash_success_rate_per_match: Union[float, None] = Field(
        None,
        alias="Flash Success Rate per Match",
    )


# Defines the PlayerInfo model for player information including detailed statistics
class PlayerInfo(BaseModel):
    # FACEIT player ID, required field with alias "player_id"
    faceit_player_id: str = Field(..., alias="player_id")

    # Player's FACEIT nickname, required field with alias "nickname"
    faceit_nickname: str = Field(..., alias="nickname")

    # Nested PlayerStats object containing detailed player statistics, required field with alias "player_stats"
    player_stats: PlayerStats = Field(..., alias="player_stats")
