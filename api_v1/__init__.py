from fastapi import APIRouter

from api_v1.project_classes.team.views import router as team_router

# from api_v1.project_classes.match.views import router as match_router
# from api_v1.project_classes.player.views import router as player_router
# from api_v1.project_classes.tournament.views import router as tournament_router
#
# from api_v1.faceit_classes.match_info.views import router as match_info_router

router = APIRouter()
# router.include_router(router=player_router, prefix="/players")
router.include_router(router=team_router, prefix="/teams")
# router.include_router(router=match_router, prefix="/matches")
# router.include_router(router=tournament_router, prefix="/tournaments")
# router.include_router(router=match_info_router, prefix="/match_info")
