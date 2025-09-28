from pydantic import BaseModel
from dotenv import load_dotenv
from enum import Enum
import os

load_dotenv()


DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER',default='postgres')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('HOST',default='localhost')}:{os.getenv('PORT',default='5432')}/{os.getenv('NAME_DB')}"

