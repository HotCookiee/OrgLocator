from  db.connection import Database
from  sqlalchemy.sql import select
from models import * 
from uuid import UUID




async def get_objects_from_database(object_table, object_id: str | None = None):
    async with Database().get_session() as session:

        if object_id is not None:
            select_object = await session.execute(select(object_table).where(object_table.id == UUID(object_id)))
            return select_object.scalars().all()
        else:
            select_object = await session.execute(select(object_table))
            return select_object.scalars().first()


        

