from datetime import datetime

import requests
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes.match.crud import update_general_match_info
from ravenspedia.api_v1.project_classes.match.dependencies import (
    find_steam_id_by_faceit_id,
)
from ravenspedia.api_v1.project_classes.match.schemes import MatchGeneralInfoUpdate
from ravenspedia.api_v1.project_classes.match_stats.helpers import sync_player_tournaments
from ravenspedia.api_v1.project_classes.player.crud import create_player
from ravenspedia.api_v1.project_classes.player.schemes import PlayerCreate
from ravenspedia.api_v1.schedules.schedule_updater import manual_update_match_status
from ravenspedia.core import TableMatch, TablePlayer, TableMatchStats
from ravenspedia.core.config import faceit_settings
from ravenspedia.core.faceit_models import PlayerStats
from ravenspedia.core.project_models.table_match import MatchStatus


async def find_start_time_from_faceit_match(
    faceit_match_id: str,
) -> datetime:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {faceit_settings.api_key}",
    }
    response = requests.get(
        f"{faceit_settings.base_url}/matches/{faceit_match_id}",
        headers=headers,
    )
    unix_time = response.json()["started_at"]
    time = datetime.fromtimestamp(unix_time)
    formatted_date = time.replace(second=0, microsecond=0)

    return formatted_date


async def add_match_stats_from_faceit(
    session: AsyncSession,
    match: TableMatch,
    faceit_url: str,
) -> TableMatch:
    if match.stats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statistics have already been added to the match {match.id}",
        )

    start = faceit_url.find("/room/") + len("/room/")
    faceit_match_id = faceit_url.replace("/scoreboard", "")[start:]

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {faceit_settings.api_key}",
    }
    response = requests.get(
        f"{faceit_settings.base_url}/matches/{faceit_match_id}/stats",
        headers=headers,
    )
    data = response.json()

    # In the json response from faceit, both bo1 and bo2 matches are marked as bo2
    if data["rounds"][0]["best_of"] == "2" and len(data["rounds"]) == 1:
        data["rounds"][0]["best_of"] = "1"

    if int(data["rounds"][0]["best_of"]) != match.best_of:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The best_of field differs from the specified one. Needed {match.best_of}, but passed {data["rounds"][0]["best_of"]}",
        )

    # Update the starting time of the match
    match = await update_general_match_info(
        session=session,
        match=match,
        match_update=MatchGeneralInfoUpdate(
            date=await find_start_time_from_faceit_match(
                faceit_match_id=faceit_match_id,
            )
        ),
    )

    response = await manual_update_match_status(
        match.id,
        MatchStatus.COMPLETED,
        session,
    )

    for round_data in data["rounds"]:
        for team_data in round_data["teams"]:
            for player_data in team_data["players"]:
                player_data["player_stats"]["round_of_match"] = round_data[
                    "match_round"
                ]
                player_data["player_stats"]["match_id"] = match.id
                player_data["player_stats"]["map"] = round_data["round_stats"]["Map"]
                result = await session.execute(
                    select(TablePlayer).filter_by(faceit_id=player_data["player_id"])
                )
                player = result.scalars().first()
                if not player:
                    player = await create_player(
                        session=session,
                        player_in=PlayerCreate(
                            nickname=player_data["nickname"],
                            steam_id=await find_steam_id_by_faceit_id(
                                faceit_id=player_data["player_id"]
                            ),
                        ),
                    )
                player_data["player_stats"]["nickname"] = player.nickname
                player_stats = PlayerStats(**player_data["player_stats"])
                round_player_stats = TableMatchStats(
                    player=player,
                    match=match,
                    match_stats=player_stats.model_dump(by_alias=True),
                )
                session.add(round_player_stats)
                await sync_player_tournaments(session, player)

    await session.flush()
    await session.commit()

    return match
