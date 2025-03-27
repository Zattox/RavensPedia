from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.project_classes.match_stats.schemes import MapPickBanInfo
from ravenspedia.core import TableMatch, TableMapPickBanInfo


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
