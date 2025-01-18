import requests
from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableMatch, TableTeam, TablePlayer, TablePlayerStats
from ravenspedia.core.config import faceit_settings
from ravenspedia.core.faceit_models import PlayerInfo
from .crud import table_to_response_form
from ravenspedia.api_v1.project_classes.player.crud import create_player
from .dependencies import find_steam_id_by_faceit_id
from .schemes import ResponseMatch
from ..player.schemes import PlayerCreate


async def add_team_in_match(
    session: AsyncSession,
    match: TableMatch,
    team: TableTeam,
) -> ResponseMatch:

    if team in match.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {team.name} already exists",
        )

    if len(match.teams) == match.max_number_of_teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of teams will participate in the match",
        )

    match.teams.append(team)

    await session.commit()

    return table_to_response_form(match=match)


async def delete_team_from_match(
    session: AsyncSession,
    match: TableMatch,
    team: TableTeam,
) -> ResponseMatch:

    if not team in match.teams:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The team is no longer participate in the match",
        )

    match.teams.remove(team)

    await session.commit()

    return table_to_response_form(match=match)


async def add_match_stats_from_faceit(
    session: AsyncSession,
    match: TableMatch,
    faceit_url: str,
) -> ResponseMatch:
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
    for round_data in data["rounds"]:
        for team_data in round_data["teams"]:
            for player_data in team_data["players"]:
                player_data["player_stats"]["nickname"] = player_data["nickname"]
                player_data["player_stats"]["round"] = round_data["match_round"]
                player_info = PlayerInfo(**player_data)
                result = await session.execute(
                    select(TablePlayer).filter_by(
                        faceit_id=player_info.faceit_player_id
                    )
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

                player_stats = TablePlayerStats(
                    player=player,
                    match=match,
                    **player_info.player_stats.model_dump(),
                )
                session.add(player_stats)

    await session.flush()
    await session.commit()
    return table_to_response_form(match=match)


async def delete_match_stats(
    session: AsyncSession,
    match: TableMatch,
) -> ResponseMatch:
    await session.execute(
        delete(TablePlayerStats).where(TablePlayerStats.match_id == match.id)
    )
    await session.commit()
    await session.refresh(match)

    return table_to_response_form(match)
