from fastapi import APIRouter

from ravenspedia.api_v1.auth.views import router as auth_router
from ravenspedia.api_v1.news.views import router as news_router
from ravenspedia.api_v1.project_classes.match.views import (
    router as match_router,
    manager_match_router,
)
from ravenspedia.api_v1.project_classes.match_stats.views import (
    router as match_stats_router,
    info_router as match_info_router,
)
from ravenspedia.api_v1.project_classes.player.views import router as player_router
from ravenspedia.api_v1.project_classes.player_stats.views import (
    router as player_stats_router,
)
from ravenspedia.api_v1.project_classes.team.views import (
    router as team_router,
    manager_team_router,
)
from ravenspedia.api_v1.project_classes.team_stats.views import (
    router as team_stats_router,
)
from ravenspedia.api_v1.project_classes.tournament.views import (
    router as tournament_router,
    manager_tournament_router,
)
from ravenspedia.api_v1.schedules.views import router as schedule_router

router = APIRouter()
router.include_router(router=auth_router, prefix="/auth")
router.include_router(router=player_router, prefix="/players")
router.include_router(router=player_stats_router, prefix="/players/stats")
router.include_router(router=team_router, prefix="/teams")
router.include_router(router=manager_team_router, prefix="/teams")
router.include_router(router=team_stats_router, prefix="/teams/stats")
router.include_router(router=match_router, prefix="/matches")
router.include_router(router=manager_match_router, prefix="/matches")
router.include_router(router=match_stats_router, prefix="/matches/stats")
router.include_router(router=match_info_router, prefix="/matches/stats")
router.include_router(router=tournament_router, prefix="/tournaments")
router.include_router(router=manager_tournament_router, prefix="/tournaments")
router.include_router(router=schedule_router, prefix="/schedules")
router.include_router(router=news_router, prefix="/news")
