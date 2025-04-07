from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.core import TableTeam, TablePlayer, PlayerTournamentAssociation


async def calculate_team_faceit_elo(
    team: TableTeam,
    session: AsyncSession,
) -> None:
    """
    Calculate the average Faceit Elo for a team based on its players' Elo.
    """
    sum_elo: int = 0
    players_with_elo: int = 0

    # Sum the Faceit Elo of all players who have a valid Elo
    for player in team.players:
        if player.faceit_elo is not None:
            sum_elo += player.faceit_elo
            players_with_elo += 1

    # If no players have Elo or the sum is 0, set the average to None
    if sum_elo == 0 or players_with_elo == 0:
        setattr(team, "average_faceit_elo", None)
    else:
        # Calculate the average Elo and set it on the team
        setattr(team, "average_faceit_elo", sum_elo / players_with_elo)

    await session.commit()


async def add_player_in_team(
    session: AsyncSession,
    team: TableTeam,
    player: TablePlayer,
) -> TableTeam:
    """
    Add a player to a team.
    """
    # Check if the player is already in the team
    if player in team.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player {player.nickname} already exists",
        )

    # Check if the player is already in another team
    if player.team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The player {player.nickname} has already joined {player.team.name}",
        )

    # Check if the team has reached its maximum player limit
    if len(team.players) == team.max_number_of_players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum number of players will participate in team",
        )

    # Add the player to the team
    team.players.append(player)
    await session.commit()

    # Recalculate the team's average Faceit Elo
    await calculate_team_faceit_elo(team, session)

    return team


async def delete_player_from_team(
    session: AsyncSession,
    team: TableTeam,
    player: TablePlayer,
) -> TableTeam:
    """
    Remove a player from a team.
    """
    # Check if the player is in the team
    if player not in team.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The player is no longer participate in the team {team.name}",
        )

    # Remove the player from the team and clear their team association
    team.players.remove(player)
    player.team_id = None
    player.team = None

    # Remove the player's association with tournaments the team is in
    await session.execute(
        delete(PlayerTournamentAssociation).where(
            PlayerTournamentAssociation.player_id == player.id,
            PlayerTournamentAssociation.tournament_id.in_(
                tournament.id for tournament in team.tournaments
            ),
        )
    )
    await session.commit()

    # Recalculate the team's average Faceit Elo
    await calculate_team_faceit_elo(team, session)

    return team
