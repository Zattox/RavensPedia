from fastapi import APIRouter

from schemes.player.scheme import Player

router = APIRouter(tags=['Player'])

@router.get("/{player_id}")
async def get_player(player_id:int, player: Player):
    return {"player_id": player_id,
            "nickname": player.nickname,
            "name": player.name, "surname": player.surname,
            "team": player.team, "matches": player.matches}