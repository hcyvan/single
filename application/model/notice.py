from sqlalchemy import Column, String, Integer

from . import BaseModel


class Notice(BaseModel):
    id = Column(String(36), primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(128))
    cell = Column(String(64))
    point = Column(Integer)

    exclude_fields = ['password']

