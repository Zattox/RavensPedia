from pydantic import BaseModel, Field


class PlayerStats(BaseModel):
    # ------------------General Stats------------------
    kills: int = Field(..., alias="Kills")  # Number of kills per match
    assists: int = Field(..., alias="Assists")  # Number of assists per match
    deaths: int = Field(..., alias="Deaths")  # Number of deaths per match
    headshots: int = Field(..., alias="Headshots")  # Number of headshots per match
    adr: float = Field(..., alias="ADR")  # Average damage per round

    # -----------------Additional Stats----------------- #
    mvps: int = Field(
        ..., alias="MVPs"
    )  # Number of awards for the "Most Valuable Player" per match
    damage: int = Field(..., alias="Damage")  # Total amount of damage done per match
    headshots_percentage: int = Field(
        ..., alias="Headshots %"
    )  # The percentage of kills per head
    kd: float = Field(..., alias="K/D Ratio")  # Kills divided by deaths (K/D)
    kpr: float = Field(..., alias="K/R Ratio")  # Kills divided by rounds (KPR)

    # --------------------Multikills-------------------- #
    double: int = Field(
        ..., alias="Double Kills"
    )  # The number of rounds where exactly 2 kills were made
    triple: int = Field(
        ..., alias="Triple Kills"
    )  # The number of rounds where exactly 3 kills were made
    quadro: int = Field(
        ..., alias="Quadro Kills"
    )  # The number of rounds where exactly 4 kills were made
    penta: int = Field(
        ..., alias="Penta Kills"
    )  # The number of rounds where exactly 5 kills were made

    # ----------------------Clutch---------------------- #
    clutch_kills: int = Field(..., alias="Clutch Kills")  # The number of clutch kills
    count_1v1: int = Field(..., alias="1v1Count")  # Number of clutch situations 1vs1
    count_1v2: int = Field(..., alias="1v2Count")  # Number of clutch situations 1vs2
    wins_1v1: int = Field(
        ..., alias="1v1Wins"
    )  # Number of wins in a 1vs1 clutch situation
    wins_1v2: int = Field(
        ..., alias="1v2Wins"
    )  # Number of wins in a 1vs2 clutch situation
    match_1v1_win_rate: float = Field(
        ..., alias="Match 1v1 Win Rate"
    )  # Win rate in 1vs1
    match_1v2_win_rate: float = Field(
        ..., alias="Match 1v2 Win Rate"
    )  # Win rate in 1vs2

    # ---------------------Entries--------------------- #
    first_kills: int = Field(..., alias="First Kills")  # The number of first kill
    entry_count: int = Field(..., alias="Entry Count")  # The number of first duels
    entry_wins: int = Field(
        ..., alias="Entry Wins"
    )  # The number of wins in the first duels
    match_entry_rate: float = Field(
        ..., alias="Match Entry Rate"
    )  # The number of participants in the first duels
    match_entry_success_rate: float = Field(
        ..., alias="Match Entry Success Rate"
    )  # Win rate in the first duels

    # ----------------------Sniper---------------------- #
    sniper_kills: int = Field(..., alias="Sniper Kills")  # Number of sniper kills
    sniper_kill_rate_per_round: float = Field(
        ..., alias="Sniper Kill Rate per Round"
    )  # Number of sniper kills per round
    sniper_kill_rate_per_match: float = Field(
        ..., alias="Sniper Kill Rate per Match"
    )  # ???

    # ------------------Special Kills------------------ #
    pistol_kills: float = Field(..., alias="Pistol Kills")  # Number of pistol kills
    knife_kills: int = Field(..., alias="Knife Kills")  # Number of knife kills
    zeus_kills: float = Field(..., alias="Zeus Kills")  # Number of zeus kills

    # ---------------------Utility--------------------- #
    utility_count: int = Field(..., alias="Utility Count")  # Number of utility
    utility_successes: int = Field(
        ..., alias="Utility Successes"
    )  # Number of helpful utility
    utility_enemies: int = Field(..., alias="Utility Enemies")  # ???
    utility_damage: int = Field(..., alias="Utility Damage")  # Utility damage per match

    # --------------Average Utility Stats-------------- #
    utility_usage_per_round: float = Field(..., alias="Utility Usage per Round")
    utility_damage_success_rate_per_match: float = Field(
        ..., alias="Utility Damage Success Rate per Match"
    )
    utility_successes_rate_per_match: float = Field(
        ..., alias="Utility Success Rate per Match"
    )
    utility_damage_per_round_in_a_match: float = Field(
        ..., alias="Utility Damage per Round in a Match"
    )

    # ----------------------Flash---------------------- #
    flash_count: int = Field(..., alias="Flash Count")  # Number of flash
    enemies_flashed: int = Field(
        ..., alias="Enemies Flashed"
    )  # The number of enemies blinded by the flash
    flash_successes: int = Field(
        ..., alias="Flash Successes"
    )  # Number of helpful flash

    # ---------------Average Flash Stats--------------- #
    flashes_per_round_in_a_match: float = Field(
        ..., alias="Flashes per Round in a Match"
    )
    enemies_flashed_per_round_in_a_match: float = Field(
        ..., alias="Enemies Flashed per Round in a Match"
    )
    flash_success_rate_per_match: float = Field(
        ..., alias="Flash Success Rate per Match"
    )

    # ------------------Result Match------------------ #
    result: int = Field(..., alias="Result")  # Did the player win this match?


class PlayerInfo(BaseModel):
    faceit_player_id: str = Field(..., alias="player_id")
    faceit_nickname: str = Field(..., alias="nickname")
    player_stats: PlayerStats = Field(..., alias="player_stats")
