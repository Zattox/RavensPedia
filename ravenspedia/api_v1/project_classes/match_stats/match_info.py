from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes.match_stats.schemes import (
    MapPickBanInfo,
    MapResultInfo,
)
from ravenspedia.core import TableMatch, TableMapPickBanInfo
from ravenspedia.core.project_models.table_match_info import (
    MapStatus,
    TableMapResultInfo,
)


async def add_pick_ban_info_in_match(
    session: AsyncSession,
    match: TableMatch,
    info: MapPickBanInfo,
) -> TableMatch:
    if len(match.veto) >= 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add more than 7 pick/ban entries for a match.",
        )

    team_names = {team.name for team in match.teams}
    if info.initiator not in team_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Initiator must be one of the teams in the match: {', '.join(team_names)}",
        )

    maps = {elem.map for elem in match.veto}
    if info.map in maps:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Map {info.map.value} must be once in the match veto",
        )

    new_pick_ban = TableMapPickBanInfo(**info.model_dump())
    match.veto.append(new_pick_ban)

    await session.commit()
    await session.refresh(match)

    return match


async def delete_last_pick_ban_info_from_match(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    if not match.veto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pick/ban entries exist to delete.",
        )

    match.veto.pop()
    await session.commit()
    await session.refresh(match)
    return match


async def add_map_result_info_in_match(
    session: AsyncSession,
    match: TableMatch,
    info: MapResultInfo,
) -> TableMatch:
    if len(match.result) >= match.best_of:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot add more than {match.best_of} map result entries for this match.",
        )

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

    team_names = {team.name for team in match.teams}
    if info.first_team not in team_names or info.second_team not in team_names:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Teams must be one of: {', '.join(team_names)}",
        )

    if info.first_half_score_first_team + info.first_half_score_second_team != 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The sum of first half scores for both teams must equal 12.",
        )

    if (
        info.first_half_score_first_team + info.second_half_score_first_team
        != info.total_score_first_team
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="First team's total score must equal the sum of first and second half scores.",
        )
    if (
        info.first_half_score_second_team + info.second_half_score_second_team
        != info.total_score_second_team
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Second team's total score must equal the sum of first and second half scores.",
        )

    if max(info.total_score_first_team, info.total_score_second_team) < 13:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The maximum total score of the two teams must be at least 13.",
        )

    new_result = TableMapResultInfo(**info.model_dump())
    match.result.append(new_result)
    await session.commit()
    await session.refresh(match)
    return match


async def delete_last_map_result_info_from_match(
    session: AsyncSession,
    match: TableMatch,
) -> TableMatch:
    if not match.result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No map result entries exist to delete.",
        )

    match.result.pop()
    await session.commit()
    await session.refresh(match)
    return match
