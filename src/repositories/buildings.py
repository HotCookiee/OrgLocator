from db.connection import Database
from sqlalchemy.sql import select
from models import * 
from uuid import UUID


async def get_list_organization_by_building(building_id: str):
    async with Database().get_session() as session:
        builds_result = await session.execute(select(Organizations).where(Organizations.building_id == UUID(building_id)))
        return builds_result.scalars().all()



