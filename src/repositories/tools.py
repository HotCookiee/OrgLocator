from db.connection import Database
from sqlalchemy.sql import select, delete
from models import *
from uuid import UUID
from asyncio import sleep
from functools import wraps


def make_query_to_the_database(func):
    '''Получение сессии базы данных для выполнения запросов к ней'''
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with Database().get_session() as session:
            result = await func(*args, **kwargs, session=session)
            return result

    return wrapper


@make_query_to_the_database
async def get_objects_from_database(
    object_table, object_id: str | None = None, session=None
):
    if object_id is not None:
        select_object = await session.execute(
            select(object_table).where(object_table.id == UUID(object_id))
        )
        return select_object.scalars().all()
    else:
        select_object = await session.execute(select(object_table))
        return select_object.scalars().first()


@make_query_to_the_database
async def add_object_to_the_database(orm_table_schema, session=None):
    try:
        session.add(orm_table_schema)
        await session.commit()
        await session.refresh(orm_table_schema)
        return {"code": 200, "message": "object added"}
    except Exception as e:
        await session.rollback()
        return {"code": 500, "message": str(e)}


@make_query_to_the_database
async def del_object_to_the_database(orm_table_schema, object_id: str, session=None):
    try:
        await session.execute(
            delete(orm_table_schema).where(orm_table_schema.id == UUID(object_id))
        )
        await session.commit()
        return {"code": 200, "message": "object deleted"}
    except Exception as e:
        await session.rollback()
