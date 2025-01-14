from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import table_to_response_form
from .schemes import ResponseMatch

from ravenspedia.core import TableMatch, TableTeam, TablePlayer


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
    for player in team.players:
        match.players.append(player)

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
    for player in team.players:
        if player in match.players:
            match.players.remove(player)

    await session.commit()

    return table_to_response_form(match=match)


async def add_player_in_match(
    session: AsyncSession,
    match: TableMatch,
    player: TablePlayer,
) -> ResponseMatch:
    if player in match.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team {player.nickname} already exists",
        )

    if len(match.players) == match.max_number_of_players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of players will participate in the match",
        )

    match.players.append(player)
    await session.commit()

    return table_to_response_form(match=match)


async def delete_player_from_match(
    session: AsyncSession,
    match: TableMatch,
    player: TablePlayer,
) -> ResponseMatch:

    if not player in match.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The player is no longer participate in the match",
        )

    match.players.remove(player)
    await session.commit()

    return table_to_response_form(match=match)
