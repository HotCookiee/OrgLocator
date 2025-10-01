from  db.connection import Database
from  sqlalchemy.sql import select,delete
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


        
async def add_object_to_the_database(orm_table_schema):
    async with Database().get_session() as session:
        try:
            session.add(orm_table_schema)
            await session.commit()
            await session.refresh(orm_table_schema)
            return {"code": 200, "message": "object added"}
        except Exception as e:
            await session.rollback()
            return {"code": 500, "message": str(e)}
        

async def del_object_to_the_database(orm_table_schema, object_id: str):
    async with Database().get_session() as session:
        try:
            await session.execute(delete(orm_table_schema).where(orm_table_schema.id == UUID(object_id)))
            await session.commit()
            return {"code": 200, "message": "object deleted"}
        except Exception as e:
            await session.rollback()



    
