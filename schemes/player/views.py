from fastapi import APIRouter

from schemes.player.schema import Player

router = APIRouter(tags=['Player'])

@router.get("/")
async def get_player(
    player: Player
):
    return {"player_id": player.id,
            "nickname": player.nickname,
            "name": player.name, "surname": player.surname,
            "team": player.team, "matches": player.matches}