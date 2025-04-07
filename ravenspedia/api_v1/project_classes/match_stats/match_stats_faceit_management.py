from datetime import datetime

import requests
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.schedules.schedule_updater import manual_update_match_status
from ravenspedia.core import (
    TableMatch,
    TablePlayer,
    TableMatchStats,
    PlayerStats,
    MatchStatus,
)
from ravenspedia.core.config import faceit_settings
from .helpers import sync_player_tournaments
from ..match.crud import update_general_match_info
from ..match.dependencies import find_steam_id_by_faceit_id
from ..match.schemes import MatchGeneralInfoUpdate
from ..player.crud import create_player
from ..player.schemes import PlayerCreate

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {faceit_settings.api_key}",
}


async def find_start_time_from_faceit_match(
    faceit_match_id: str,
) -> datetime:
    """
    Retrieve the start time of a Faceit match using the Faceit API.
    """
    response = requests.get(
        f"{faceit_settings.base_url}/matches/{faceit_match_id}",
        headers=headers,
    )

    # Check if the API request was successful
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve match start time from Faceit API",
        )

    # Extract and format the start time
    unix_time = response.json()["started_at"]
    time = datetime.fromtimestamp(unix_time)
    formatted_date = time.replace(second=0, microsecond=0)

    return formatted_date


async def add_match_stats_from_faceit(
    session: AsyncSession,
    match: TableMatch,
    faceit_url: str,
) -> TableMatch:
    """
    Add match stats from a Faceit match to the database.
    """
    # Check if the match already has stats
    if match.stats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statistics have already been added to the match {match.id}",
        )

    setattr(match, "original_source", faceit_url)

    # Extract the Faceit match ID from the URL
    start = faceit_url.find("/room/") + len("/room/")
    if start == -1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Faceit URL format",
        )
    faceit_match_id = faceit_url.replace("/scoreboard", "")[start:]

    response = requests.get(
        f"{faceit_settings.base_url}/matches/{faceit_match_id}/stats",
        headers=headers,
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve stats from Faceit API",
        )
    data = response.json()

    # Adjust best_of for BO1 matches (Faceit API marks BO1 as BO2)
    if data["rounds"][0]["best_of"] == "2" and len(data["rounds"]) == 1:
        data["rounds"][0]["best_of"] = "1"

    # Validate best_of value
    if int(data["rounds"][0]["best_of"]) != match.best_of:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The best_of field differs from the specified one. Needed {match.best_of}, but passed {data["rounds"][0]["best_of"]}",
        )

    # Update the match start time using the Faceit match start time
    match = await update_general_match_info(
        session=session,
        match=match,
        match_update=MatchGeneralInfoUpdate(
            date=await find_start_time_from_faceit_match(
                faceit_match_id=faceit_match_id,
            )
        ),
    )

    # Update the match status to COMPLETED
    await manual_update_match_status(
        match=match,
        new_status=MatchStatus.COMPLETED,
        session=session,
    )

    # Process each round and player stats from the Faceit data
    for round_data in data["rounds"]:
        for team_data in round_data["teams"]:
            for player_data in team_data["players"]:
                player_data["player_stats"]["round_of_match"] = round_data[
                    "match_round"
                ]
                player_data["player_stats"]["match_id"] = match.id
                player_data["player_stats"]["map"] = round_data["round_stats"]["Map"]

                # Find or create the player in the database
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
                await sync_player_tournaments(session=session, player=player)

    await session.flush()
    await session.commit()

    return match
