from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect


class BASE(DeclarativeBase):

    @staticmethod
    def object_to_dict(obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
