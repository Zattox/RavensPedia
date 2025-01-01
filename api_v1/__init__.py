from fastapi import APIRouter

from .player.views import router as player_router
from .team.views import router as team_router
from .match.crud import router as match_router
from .tournament.views import router as tournament_router
router = APIRouter()
router.include_router(router=player_router, prefix='/players')
router.include_router(router=team_router, prefix='/teams')
router.include_router(router=match_router, prefix='/matches')
router.include_router(router=tournament_router, prefix='/tournaments')