from fastapi import APIRouter

from ravenspedia.api_v1.demo_auth.demo_jwt_auth import router as demo_jwt_auth_router
from ravenspedia.api_v1.demo_auth.views import router as demo_auth_router
from ravenspedia.api_v1.project_classes.match.views import (
    router as match_router,
    manager_match_router,
)
from ravenspedia.api_v1.project_classes.player.views import router as player_router
from ravenspedia.api_v1.project_classes.team.views import (
    router as team_router,
    manager_team_router,
)
from ravenspedia.api_v1.project_classes.tournament.views import (
    router as tournament_router,
    manager_tournament_router,
)
from ravenspedia.api_v1.schedules.views import router as schedule_router

router = APIRouter()
router.include_router(router=demo_auth_router, prefix="/demo_auth")
router.include_router(router=demo_jwt_auth_router, prefix="/demo_auth")
router.include_router(router=player_router, prefix="/players")
router.include_router(router=team_router, prefix="/teams")
router.include_router(router=manager_team_router, prefix="/teams")
router.include_router(router=match_router, prefix="/matches")
router.include_router(router=manager_match_router, prefix="/matches")
router.include_router(router=tournament_router, prefix="/tournaments")
router.include_router(router=manager_tournament_router, prefix="/tournaments")
router.include_router(router=schedule_router, prefix="/schedules")
