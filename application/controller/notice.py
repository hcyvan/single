from flask import request
from flask_login import login_required, current_user

from . import api
from ..model.notice import Notice
from ..helper import response_json, parse_model_list
from ..service import notice_service
from config.constant import NoticeStatus
from config.status_code import *


@api.route('/notice', methods=['GET'])
@login_required
def get_notices():
    scope = int(request.args.get('scope', 0))
    query = Notice.query.filter_by(receiver_id=current_user.id)
    if scope == 1:
        query = query.filter_by(is_read=NoticeStatus.unread.value)
    elif scope == 2:
        query = query.filter_by(is_read=NoticeStatus.read.value)
    notices = query.all()
    return response_json(data=parse_model_list(notices))


@api.route('/notice/<notice_id>', methods=['GET'])
@login_required
def get_notice(notice_id):
    notice = Notice.query.get(notice_id)
    if not notice:
        return response_json(NOTICE_NOT_EXIST)
    if notice.receiver_id != current_user.id:
        return response_json(NO_PERMISSION)
    if notice.is_read == NoticeStatus.unread.value:
        notice.is_read = NoticeStatus.read.value
        notice.save()
    return response_json(data=notice_service.format_notice(notice))
