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

