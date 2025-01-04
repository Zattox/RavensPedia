from sqlalchemy.orm import Mapped


class PlayerStats:
    # ------------------General Stats------------------
    kills: Mapped[int]  # Number of kills per match
    assists: Mapped[int]  # Number of assists per match
    deaths: Mapped[int]  # Number of deaths per match
    headshots: Mapped[int]  # Number of headshots per match
    adr: Mapped[float]  # Average damage per round

    # -----------------Additional Stats----------------- #
    mvps: Mapped[int]  # Number of awards for the "Most Valuable Player" per match
    damage: Mapped[int]  # Total amount of damage done per match
    headshots_percentages: Mapped[int]  # The percentage of kills per head
    kills_deaths_ratio: Mapped[float]  # Kills divided by deaths (K/D)
    kills_per_round_ratio: Mapped[float]  # Kills divided by rounds (KPR)

    # --------------------Multikills-------------------- #
    double_kills: Mapped[int]  # The number of rounds where exactly 2 kills were made
    triple_kills: Mapped[int]  # The number of rounds where exactly 3 kills were made
    quadro_kills: Mapped[int]  # The number of rounds where exactly 4 kills were made
    penta_kills: Mapped[int]  # The number of rounds where exactly 5 kills were made

    # ----------------------Clutch---------------------- #
    clutch_kills: Mapped[int]  # The number of clutch kills
    _1v1count: Mapped[int]  # Number of clutch situations 1vs1
    _1v2count: Mapped[int]  # Number of clutch situations 1vs2
    _1v1Wins: Mapped[int]  # Number of wins in a 1vs1 clutch situation
    _1v2Wins: Mapped[int]  # Number of wins in a 1vs2 clutch situation
    match_1v1_win_rate: Mapped[float]  # Win rate in 1vs1
    match_1v2_win_rate: Mapped[float]  # Win rate in 1vs2

    # ---------------------Entries--------------------- #
    first_kills: Mapped[int]  # The number of first kill
    entry_count: Mapped[int]  # The number of first duels
    entry_wins: Mapped[int]  # The number of wins in the first duels
    match_entry_rate: Mapped[float]  # The number of participants in the first duels
    match_entry_success_rate: Mapped[float]  # Win rate in the first duels

    # ----------------------Sniper---------------------- #
    sniper_kills: Mapped[int]  # Number of sniper kills
    sniper_kill_rate_per_round: Mapped[float]  # Number of sniper kills per round
    sniper_kill_rate_per_match: Mapped[float]  # ???

    # ------------------Special Kills------------------ #
    pistol_kills: Mapped[float]  # Number of pistol kills
    knife_kills: Mapped[int]  # Number of knife kills
    zeus_kills: Mapped[float]  # Number of zeus kills

    # ---------------------Utility--------------------- #
    utility_count: Mapped[int]  # Number of utility
    utility_successes: Mapped[int]  # Number of helpful utility
    utility_enemies: Mapped[int]  # ???
    utility_damage: Mapped[int]  # Utility damage per match

    # --------------Average Utility Stats-------------- #
    utility_usage_per_round: Mapped[float]
    utility_damage_success_rate_per_match: Mapped[float]
    utility_successes_rate_per_match: Mapped[float]
    utility_damage_per_round_in_a_match: Mapped[float]

    # ----------------------Flash---------------------- #
    flash_count: Mapped[int]  # Number of flash
    enemies_flashed: Mapped[int]  # The number of enemies blinded by the flash
    flash_successes: Mapped[int]  # Number of helpful flash

    # ---------------Average Flash Stats--------------- #
    flashes_per_round_in_a_match: Mapped[float]
    enemies_flashed_per_round_in_a_match: Mapped[float]
    flash_success_rate_per_match: Mapped[float]

    # ------------------Result Match------------------ #
    result: Mapped[int]  # Did the player win this match?


class PlayerInfo:
    faceit_player_id: Mapped[str]
    faceit_nickname: Mapped[str]
    player_stats: PlayerStats
