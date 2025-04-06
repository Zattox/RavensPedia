from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemes import MapPickBanInfo, MapResultInfo
from ravenspedia.core import TableMatch, TableMapPickBanInfo, MapStatus, TableMapResultInfo

async def add_pick_ban_info_in_match(
    session: AsyncSession,
    match: TableMatch,
    info: MapPickBanInfo,
) -> TableMatch:
    """
    Add pick/ban information to a match with validation checks.
    """
    # Check if the veto list has reached the maximum limit of 7 entries
    if len(match.veto) >= 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add more than 7 pick/ban entries for a match.",
        )

    # Validate that the initiator is one of the teams in the match
    team_names = {team.name for team in match.teams}
    if info.initiator not in team_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Initiator must be one of the teams in the match: {', '.join(team_names)}",
        )

    # Check for duplicate maps in the veto list
    maps = {elem.map for elem in match.veto}
    if info.map in maps:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Map {info.map.value} must be once in the match veto",
        )

    # Add the new pick/ban info to the match
    new_pick_ban = TableMapPickBanInfo(**info.model_dump())
    match.veto.append(new_pick_ban)

    await session.commit()
    await session.refresh(match)

    return match

async def delete_last_pick_ban_info_from_match(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    """
    Delete the last pick/ban information from a match.
    """

    # If the veto list is empty, return the match as is
    if not match.veto:
        return match

    # Remove the last pick/ban entry
    match.veto.pop()
    await session.commit()
    await session.refresh(match)
    return match

async def add_map_result_info_in_match(
    session: AsyncSession,
    match: TableMatch,
    info: MapResultInfo,
) -> TableMatch:
    """
    Add map result information to a match with validation checks.
    """
    # Check if the result list has reached the best_of limit
    if len(match.result) >= match.best_of:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot add more than {match.best_of} map result entries for this match.",
        )

    # Validate that the map is in the veto list and not banned
    veto_map_dict = {veto.map: veto.map_status for veto in match.veto}
    if info.map not in veto_map_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Map {info.map.value} must be in the veto list.",
        )
    if veto_map_dict[info.map] == MapStatus.Banned:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Map {info.map.value} is banned and cannot have a result.",
        )

    # Validate the map status based on the current result count
    current_result_count = len(match.result)
    expected_status = (
        MapStatus.Default
        if current_result_count == match.best_of - 1
        else MapStatus.Picked
    )
    if veto_map_dict[info.map] != expected_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Map {info.map.value} must have status '{expected_status.value}' "
                f"({'Default' if expected_status == MapStatus.Default else 'Picked'} for position {current_result_count + 1})"
            ),
        )

    # Validate that the teams are part of the match
    team_names = {team.name for team in match.teams}
    if info.first_team not in team_names or info.second_team not in team_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Teams must be one of: {', '.join(team_names)}",
        )

    # Validate first half scores (must sum to 12)
    total_first_half_rounds = (
        info.first_half_score_first_team + info.first_half_score_second_team
    )
    if total_first_half_rounds != 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The sum of first half scores for both teams must equal 12.",
        )

    # Validate second half scores (must not exceed 12)
    total_second_half_rounds = (
        info.second_half_score_first_team + info.second_half_score_second_team
    )
    if total_second_half_rounds > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The sum of the second half scores for both teams must be less than or equal to 12.",
        )

    # Validate total scores for the first team
    total_score_first_team = (
        info.first_half_score_first_team
        + info.second_half_score_first_team
        + info.overtime_score_first_team
    )
    if total_score_first_team != info.total_score_first_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First team's total score must equal the sum of first and second half scores.",
        )

    # Validate total scores for the second team
    total_score_second_team = (
        info.first_half_score_second_team
        + info.second_half_score_second_team
        + info.overtime_score_second_team
    )
    if total_score_second_team != info.total_score_second_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Second team's total score must equal the sum of first and second half scores.",
        )

    # Validate that the maximum total score is at least 13
    if max(total_score_first_team, total_score_second_team) < 13:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum total score of the two teams must be at least 13.",
        )

    # Validate overtime score difference (must be between 0 and 4)
    winner_of_overtime = max(
        info.overtime_score_first_team, info.overtime_score_second_team
    )
    loser_of_overtime = min(
        info.overtime_score_first_team, info.overtime_score_second_team
    )
    diff = winner_of_overtime - loser_of_overtime
    if diff > 4 or diff < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect completion of overtime rounds.",
        )

    # Add the new map result to the match
    new_result = TableMapResultInfo(**info.model_dump())
    match.result.append(new_result)
    await session.commit()
    await session.refresh(match)
    return match

async def delete_last_map_result_info_from_match(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    """
    Delete the last map result information from a match.
    """
    # If the result list is empty, return the match as is
    if not match.result:
        return match

    # Remove the last map result entry
    match.result.pop()
    await session.commit()
    await session.refresh(match)
    return match