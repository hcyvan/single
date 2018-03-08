from functools import partial
from sqlalchemy.orm import joinedload

from ..model.notice import Notice
from ..model.user import Love
from config.constant import NoticeType


def format_notice(notice):
    if notice.type == NoticeType.receive_love.value or notice.type == NoticeType.love_handled.value:
        love = Love.query.options(joinedload('sender'), joinedload('receiver')).filter_by(
            id=notice.meta.get('object_id')).first()
        return dict(**notice.to_dict(), object=love.to_dict())
    return notice.to_dict()


def add_notice(notice_type, receiver_id, **kwargs):
    notice = Notice(type=notice_type, receiver_id=receiver_id)
    if notice_type == NoticeType.receive_love.value or notice_type == NoticeType.love_handled.value:
        meta = dict(
            from_name=kwargs.get('from_name'),
            from_id=kwargs.get('from_id'),
            to_name=kwargs.get('to_name'),
            to_id=kwargs.get('to_id'),
            object_id=kwargs.get('object_id')
        )
        notice.meta = meta
        notice.save()


notice_send_love = partial(add_notice, notice_type=NoticeType.receive_love.value)
notice_handle_love = partial(add_notice, notice_type=NoticeType.love_handled.value)
