import requests
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.faceit_models import MatchInfo
from .funcs import json_to_round_info
from core.config import faceit_settings


# A function for create a MatchInfo in the database
async def create_match_info(
    session: AsyncSession,
    faceit_match_id: str,
) -> MatchInfo:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {faceit_settings.faceit_api_key}",
    }
    response = requests.get(
        f"{faceit_settings.faceit_base_url}/{faceit_match_id}/stats", headers=headers
    )
    data = json_to_round_info(response.json())
    match_info_create: MatchInfo = MatchInfo(
        faceit_match_id=faceit_match_id, rounds=data
    )
    session.add(match_info_create)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(match_info)
    return match_info_create
