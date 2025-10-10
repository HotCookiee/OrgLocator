from .tools import make_query_to_the_database
from sqlalchemy.sql import select, insert,delete
from sqlalchemy.ext.asyncio import AsyncSession
from models import Users
from argon2 import PasswordHasher
from models import RefreshTokens, Users
from schemas.user import AddTokenToUser
from uuid import uuid4


ph = PasswordHasher()


class EmptyUserObject(Exception):
    pass


@make_query_to_the_database
async def get_user_by_name(name: str, session: AsyncSession = None) -> Users | None:
    result = await session.execute(select(Users).where(Users.name == name))
    return result.scalars().one_or_none()

@make_query_to_the_database
async def get_user_by_id(id: str, session: AsyncSession = None) -> Users | None:
    result = await session.execute(select(Users).where(Users.id == id))
    return result.scalars().one_or_none()

def verify_password(stored_hash: str, plain_password: str) -> bool:
    return ph.verify(stored_hash, plain_password)


@make_query_to_the_database
async def add_refresh_token(
    add_token_schema: AddTokenToUser, session: AsyncSession = None
):
    await session.execute(
        insert(RefreshTokens).values(**add_token_schema.model_dump(exclude_none=True))
    )
    await session.commit()


@make_query_to_the_database
async def get_jti_by_user_id(
    user_id: str, session: AsyncSession = None
) -> RefreshTokens | None:
    result = await session.execute(
        select(RefreshTokens).where(
            RefreshTokens.user_id == user_id, RefreshTokens.revoked == False
        )
    )
    refresh_token = result.scalars().one_or_none()
    return refresh_token



@make_query_to_the_database
async def delete_user_by_id(user_id: str, session: AsyncSession = None):
    await session.execute(delete(Users).where(Users.id == user_id))
    await session.commit()

