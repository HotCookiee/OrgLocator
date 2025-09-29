from  db.connection import Database
from  sqlalchemy.sql import select,between
from  sqlalchemy.orm import selectinload
from models import * 
from uuid import UUID


class OrganizationSearchService():
    
    @staticmethod
    async def get_list_organizations_in_the_range(latitude_min: float, latitude_max: float, longitude_min: float, longitude_max: float):
        async with Database().get_session() as session:
            select_result = await session.execute(select(Organizations).
                                                  join(Organizations.building).
                                                  options(selectinload(Organizations.building)).
                                                  where(between(Buildings.latitude,latitude_min,latitude_max),
                                                        between(Buildings.longitude,longitude_min,longitude_max)))
            
            return select_result.scalars().unique().all()

    


class GetInfoFromOrganization():

    @staticmethod
    async def get_info_organization_by_name(organization_name: str):
        async with Database().get_session() as session:
            select_result = await session.execute(select(Organizations).where(Organizations.name == organization_name))
            return select_result.scalars().unique().all()