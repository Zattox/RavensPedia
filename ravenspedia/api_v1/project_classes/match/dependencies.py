from typing import Annotated

import requests
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ravenspedia.core import (
    db_helper,
    TableMatch,
    TableMatchStats,
    TableTeam,
    TableTournament,
)
from ravenspedia.core.config import faceit_settings


async def get_match_by_id(
    match_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> TableMatch:
    """
    Retrieve a match from the database by its ID, with related data.
    """
    match = await session.scalar(
        select(TableMatch)
        .where(TableMatch.id == match_id)
        .options(
            selectinload(TableMatch.stats).selectinload(TableMatchStats.player),
            selectinload(TableMatch.teams).selectinload(TableTeam.players),
            selectinload(TableMatch.tournament).selectinload(TableTournament.teams),
            selectinload(TableMatch.veto),
            selectinload(TableMatch.result),
        ),
    )

    # Raise an exception if the match is not found
    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match {match_id} not found",
        )

    return match


async def find_steam_id_by_faceit_id(faceit_id: str) -> str:
    """
    Retrieve a player's Steam ID using their Faceit ID via the Faceit API.
    """
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {faceit_settings.api_key}",
    }
    response = requests.get(
        f"{faceit_settings.base_url}/players/{faceit_id}",
        headers=headers,
    )
    return response.json()["games"]["cs2"]["game_player_id"]
