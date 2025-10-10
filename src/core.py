from pydantic import BaseModel
from dotenv import load_dotenv
from enum import Enum
import os

load_dotenv()


DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}/{os.getenv('NAME_DB')}"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
