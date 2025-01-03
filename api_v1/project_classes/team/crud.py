from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.project_models import Team
from api_v1.project_classes.team.scheme import TeamCreate, TeamUpdatePartial


# A function to get all the Teams from the database
async def get_teams(session: AsyncSession) -> list[Team]:
    statement = select(Team).order_by(Team.id)
    result: Result = await session.execute(statement)
    teams = result.scalars().all()
    return list(teams)


# A function for getting a Team by its id from the database
async def get_team(
    session: AsyncSession,
    team_id: int,
) -> Team | None:
    return await session.get(Team, team_id)


# A function for create a Team in the database
async def create_team(
    session: AsyncSession,
    team_in: TeamCreate,
) -> Team:
    # Turning it into a Team class without Mapped fields
    team = Team(**team_in.model_dump())
    session.add(team)
    await session.commit()  # Make changes to the database
    # It is necessary if there are changes on the database side
    # await session.refresh(team)
    return team


# A function for partial update a Team in the database
async def update_team_partial(
    session: AsyncSession,
    team: Team,
    team_update: TeamUpdatePartial,
) -> Team:
    for name, value in team_update.model_dump(exclude_unset=True).items():
        setattr(team, name, value)
    await session.commit()  # Make changes to the database
    return team


# A function for delete a Team from the database
async def delete_team(
    session: AsyncSession,
    team: Team,
) -> None:
    await session.delete(team)
    await session.commit()  # Make changes to the database
