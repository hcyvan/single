from flask_login import UserMixin
from sqlalchemy import Column, String, Integer

from .base import BaseModel


class User(BaseModel, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    password = Column(String(128))
    cell = Column(String(64))
    point = Column(Integer)

    exclude_fields = ['password']


class Love(BaseModel):
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer)
    to_id = Column(Integer)
    accept = Column(Integer, comment='0 未接受 1 被接受者 2 接受者')
    commit = Column(String(256))
