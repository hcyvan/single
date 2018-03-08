from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from .base import BaseModel
from config.constant import NoticeStatus


class Notice(BaseModel):
    id = Column(Integer, primary_key=True)
    receiver_id = Column(Integer)
    type = Column(Integer)
    meta = Column(JSONB)
    is_read = Column(Integer, default=NoticeStatus.unread.value)

    exclude_fields = ['updated']

