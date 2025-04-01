from unittest.mock import patch

from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from ravenspedia.core import TableTeam, TablePlayer, PlayerTournamentAssociation


async def calculate_team_faceit_elo(
    team: TableTeam,
    session: AsyncSession,
) -> None:
    sum_elo: int = 0
    players_with_elo: int = 0
    for player in team.players:
        if player.faceit_elo is not None:
            sum_elo = sum_elo + player.faceit_elo
            players_with_elo = players_with_elo + 1
    if sum_elo == 0 or players_with_elo == 0:
        setattr(team, "average_faceit_elo", None)
    else:
        setattr(team, "average_faceit_elo", sum_elo / players_with_elo)
    await session.commit()

async def add_player_in_team(
    session: AsyncSession,
    team: TableTeam,
    player: TablePlayer,
) -> TableTeam:
    if player in team.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player {player.nickname} already exists",
        )

    if player.team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The player {player.nickname} has already joined {player.team.name}",
        )

    if len(team.players) == team.max_number_of_players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The maximum number of players will participate in team",
        )

    team.players.append(player)
    await session.commit()

    await calculate_team_faceit_elo(team, session)

    return team


async def delete_player_from_team(
    session: AsyncSession,
    team: TableTeam,
    player: TablePlayer,
) -> TableTeam:
    if player not in team.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The player is no longer participate in the team {team.name}",
        )

    team.players.remove(player)
    player.team_id = None
    player.team = None

    await session.execute(
        delete(PlayerTournamentAssociation).where(
            PlayerTournamentAssociation.player_id == player.id,
            PlayerTournamentAssociation.tournament_id.in_(
                tournament.id for tournament in team.tournaments
            ),
        )
    )
    await session.commit()

    await calculate_team_faceit_elo(team, session)

    return team
