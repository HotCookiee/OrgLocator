from src.db.connection import Database as DatabaseDB, Redis as RedisDB
from redis import Redis as RedisClient
from sqlalchemy.ext.asyncio import AsyncSession as PGSession
from sqlalchemy.sql import select, delete
from src.models import *
from uuid import UUID
from functools import wraps
from typing import Any
import json


class DataBase:
    def make_query_to_the_database(func):
        """Получение сессии базы данных для выполнения запросов к ней"""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with DatabaseDB().get_session() as session:
                result = await func(*args, **kwargs, session=session)
                return result

        return wrapper

    @make_query_to_the_database
    async def get_objects_from_database_by_id_or_name(
        object_table,
        pydantic_schema,
        determine: str,
        session: PGSession = None,
        field: str = "id",
    ):
        get_object_by_redis = await Redis().get_value_by_key(
            f"{object_table.__tablename__.lower()}_{field}_{determine}"
        )
        if get_object_by_redis is not None:
            print("From cache")
            return json.loads(get_object_by_redis)

        match field:
            case "id":
                select_object = await session.execute(
                    select(object_table).where(object_table.id == UUID(determine))
                )
                result = select_object.scalars().first()
                await Redis().set_value_by_key(
                    f"{object_table.__tablename__.lower()}_{field}_{determine}",
                    pydantic_schema.model_validate(result).model_dump_json(),
                )
                return result
            case "name":
                select_object = await session.execute(
                    select(object_table).where(object_table.name == determine)
                )
                result = select_object.scalars().all()
                await Redis().set_value_by_key(
                    f"{object_table.__tablename__.lower()}_{field}_{determine}",
                    pydantic_schema.model_validate(result).model_dump_json(),
                )
                return result
            case _:
                raise ValueError(f"Unsupported field for query: {field}")

    @make_query_to_the_database
    async def add_object_to_the_database(orm_table_schema, session: PGSession = None):
        try:
            session.add(orm_table_schema)
            await session.commit()
            await session.refresh(orm_table_schema)
            return {"code": 200, "message": "object added"}
        except Exception as e:
            await session.rollback()
            return {"code": 500, "message": str(e)}

    @make_query_to_the_database
    async def del_object_to_the_database(
        orm_table_schema, object_id: str, session: PGSession = None
    ):
        try:
            await session.execute(
                delete(orm_table_schema).where(orm_table_schema.id == UUID(object_id))
            )
            await session.commit()
            return {"code": 200, "message": "object deleted"}
        except Exception as e:
            await session.rollback()


class Redis:

    def corut_get_session(func):
        """Декоратор: получает/помещает session в kwargs, не ломая позиционные аргументы."""

        @wraps(func)
        async def wrapper(*args, **kwargs):
            session = RedisDB().get_redis()
            return await func(*args, **kwargs, session=session)

        return wrapper

    @corut_get_session
    async def get_value_by_key(
        self, key: str, session: RedisClient = None
    ) -> Any | None:
        try:
            return await session.get(key)
        except Exception as e:
            raise e

    @corut_get_session
    async def set_value_by_key(
        self,
        key: str,
        value: dict,
        session: RedisClient = None,
        life_time: int = 60,
        **kwargs,
    ):
        try:
            await session.set(key, value, ex=life_time, **kwargs)
            return True
        except Exception as e:
            raise e

    @corut_get_session
    async def del_value_by_key(self, key: str, session: RedisClient = None):
        try:
            await session.delete(key)
            return True
        except Exception as e:
            raise e
