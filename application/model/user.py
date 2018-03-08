from flask_login import UserMixin
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    password = Column(String(128))
    cell = Column(String(64), unique=True)
    point = Column(Integer)
    lover_id = Column(Integer)

    exclude_fields = ['password', 'updated']


class Love(BaseModel):
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer)
    to_id = Column(Integer)
    status = Column(Integer, comment='0 未同意 1 同意 2 拒绝 3 拉黑')
    comment = Column(String(256))

    sender = relationship('User', primaryjoin='User.id == foreign(Love.from_id)', backref='send_love')
    receiver = relationship('User', primaryjoin='User.id == foreign(Love.to_id)', backref='receive_love')

    exclude_fields = ['updated']

