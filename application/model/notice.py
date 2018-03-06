from sqlalchemy import Column, Integer, Text

from .base import BaseModel


class Notice(BaseModel):
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, unique=True)
    to_id = Column(Integer)
    content = Column(Text)
    is_read = Column(Integer)

