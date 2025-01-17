from typing import Annotated

import requests
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from ravenspedia.api_v1.faceit_classes.match_info import crud
from ravenspedia.core import db_helper
from ravenspedia.core.config import faceit_settings
from ravenspedia.core.faceit_models import RoundInfo
from .funcs import json_to_round_info
from .schemes import MatchInfo


# A function for get a match_info from the database by id
async def get_match_info_by_id(
    match_info_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> MatchInfo:
    match_info = await crud.get_match_info(session=session, match_info_id=match_info_id)
    # If such an id does not exist, then throw an exception.
    if match_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MatchInfo {match_info_id} not found",
        )
    return match_info


async def get_data_from_faceit(
    faceit_match_id: str,
) -> list[RoundInfo]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {faceit_settings.faceit_api_key}",
    }
    response = requests.get(
        f"{faceit_settings.faceit_base_url}/matches/{faceit_match_id}/stats", headers=headers
    )
    data = json_to_round_info(response.json())
    return data
