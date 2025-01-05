from core.faceit_models.round_info import RoundInfo


def json_to_round_info(data: dict) -> list[RoundInfo]:
    rounds = []
    for round_data in data.get("rounds", []):
        rounds.append(RoundInfo(**round_data))
    return rounds
