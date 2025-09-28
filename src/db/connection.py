from  sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker, AsyncSession
from sqlalchemy.sql import select
import os
from core import DATABASE_URL



class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_async_engine(DATABASE_URL, echo=True)
            cls._instance.session_factory = async_sessionmaker(bind=cls._instance.engine)
        return cls._instance

    def __del__(self):
        _instance = None

    def get_session(self) -> AsyncSession:
        return self.session_factory()
    
    
    async def is_alive(self)->bool:
        if self._instance is not None:
            try:
                async with self.get_session() as session:
                    await session.execute(select(1))
                return True
            except Exception as e: 
                return False