from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import table_to_response_form
from .schemes import ResponseTeam

from ravenspedia.core import TableTeam, TablePlayer


async def add_player_in_team(
    session: AsyncSession,
    team: TableTeam,
    player: TablePlayer,
) -> ResponseTeam:
    if player in team.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player {player.nickname} already exists",
        )

    if len(team.players) == team.max_number_of_players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of teams will participate in the match",
        )

    team.players.append(player)
    await session.commit()

    return table_to_response_form(team=team)


async def delete_player_from_team(
    session: AsyncSession,
    team: TableTeam,
    player: TablePlayer,
) -> ResponseTeam:
    if not player in team.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The player is no longer participate in the team {team.name}",
        )

    team.players.remove(player)
    await session.commit()

    return table_to_response_form(team=team)
