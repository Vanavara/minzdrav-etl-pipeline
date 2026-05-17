# third party
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(schema="nsi")


class Base(DeclarativeBase):
    metadata = metadata
