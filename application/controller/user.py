from flask import request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import joinedload

from . import api
from ..model.user import User, Love
from ..helper import response_json
from ..service import notice_service
from config.status_code import *
from config.constant import LoveStatus, NoticeType, INIT_POINT


@api.route('/login', methods=['POST'])
def login():
    password = request.json.get('password')
    cell = request.json.get('cell')
    if None in [password, cell]:
        return response_json(LOST_REQUIRED_FIELD)

    user = User.query.filter_by(cell=cell).first()
    if not user:
        return USER_NOT_EXIST
    if not check_password_hash(user.password, password):
        return USER_WRONG_PASSWORD

    login_user(user)

    return response_json(data=dict(id=user.id))


@api.route('/session', methods=['GET'])
@login_required
def session():
    return response_json(data=current_user.to_dict())


@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return response_json(SUCCESS)


@api.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    cell = request.json.get('cell')
    if None in [username, password, cell]:
        return response_json(LOST_REQUIRED_FIELD)
    user_tmp = User.query.filter_by(cell=cell).first()
    if user_tmp:
        return response_json(USER_CELL_USED)
    pw_hash = generate_password_hash(password).decode()
    user = User(
        username=username,
        password=pw_hash,
        cell=cell,
        point=INIT_POINT
    )

    user.save()
    return response_json(data=dict(id=user.id))


@api.route('/love', methods=['POST'])
@login_required
def vindicate():
    object_id = request.json.get('object_id')
    from_comment = request.json.get('from_comment', '')
    if current_user.point < 1:
        return response_json(POINT_ZERO)
    if current_user.lover_id:
        return response_json(LOVE_SENDER_HAS_LOVER)

    receiver = User.query.get(object_id)
    if not receiver:
        return response_json(LOVE_RECEIVER_NOT_EXIST)
    if receiver.lover_id:
        return response_json(LOVE_RECEIVER_HAS_LOVER)
    love_old = Love.query.filter_by(from_id=current_user.id, to_id=receiver.id).first()
    if love_old:
        if love_old.status == LoveStatus.on.value:
            return response_json(LOVE_EXIST_STATUS_ON)
        elif love_old.status == LoveStatus.mask.value:
            return response_json(LOVE_MASK)

    love = Love(
        from_id=current_user.id,
        to_id=receiver.id,
        status=LoveStatus.on.value,
        from_comment=from_comment
    )
    current_user.point = current_user.point - 1
    love.save()

    notice_service.add_notice(
        notice_type=NoticeType.love_on.value,
        receiver_id=receiver.id,
        from_name=current_user.username,
        from_id=current_user.id,
        to_name=receiver.username,
        to_id=receiver.id,
        object_id=love.id,
    )
    return response_json(SUCCESS)


@api.route('/love/<love_id>', methods=['POST'])
@login_required
def handle_love(love_id):
    attitude = request.json.get('attitude', LoveStatus.agree.value)
    to_comment = request.json.get('to_comment', '')

    love = Love.query.options(joinedload('sender'), joinedload('receiver')).filter_by(id=love_id).first()
    if not love:
        return response_json(LOVE_NOT_EXIST)
    if love.receiver.id != current_user.id:
        return response_json(LOVE_NOT_YOURS)

    if love.status == LoveStatus.on.value:
        if love.sender.lover_id:
            return response_json(LOVE_LATE)
        love.status = attitude
        love.to_comment = to_comment
        if attitude == LoveStatus.agree.value:
            love.sender.lover_id = love.receiver.id
            love.receiver.lover_id = love.sender.id
            love.receiver.point = love.receiver.point + 1
        love.save()

        notice_service.add_notice(
            notice_type=love.status,
            receiver_id=love.sender.id,
            from_name=current_user.username,
            from_id=current_user.id,
            to_name=love.sender.username,
            to_id=love.sender.id,
            object_id=love.id
        )
        return response_json(SUCCESS)
    else:
        return response_json(LOVE_HANDLED)


@api.route('/love/<love_id>', methods=['DELETE'])
@login_required
def delete_love(love_id):
    part_comment = request.json.get('part_comment')
    love = Love.query.options(joinedload('sender'), joinedload('receiver')).filter_by(id=love_id).first()
    if not love:
        return response_json(LOVE_NOT_EXIST)
    if love.status != LoveStatus.agree.value:
        return response_json(LOVE_NOT_LOVER)
    if current_user.id == love.sender.id:
        lover_id = love.receiver.id
        lover_name = love.receiver.username
    elif current_user.id == love.receiver.id:
        lover_id = love.sender.id
        lover_name = love.sender.username
    else:
        return response_json(LOVE_NOT_YOURS)

    love.sender.lover_id = None
    love.receiver.lover_id = None
    love.status = LoveStatus.part.value
    love.part_comment = part_comment
    love.part_id = current_user.id
    love.save()

    notice_service.add_notice(
        notice_type=NoticeType.love_part.value,
        receiver_id=lover_id,
        from_name=current_user.username,
        from_id=current_user.id,
        to_name=lover_name,
        to_id=lover_id,
        object_id=love.id
    )

    return response_json(SUCCESS)


@api.route('/search', methods=['GET'])
@login_required
def search():
    user_id = request.args.get('user_id')
    if current_user.point < 1:
        return response_json(POINT_ZERO)
    user = User.query.options(joinedload('lover')).filter_by(id=user_id).first()
    if not user:
        return response_json(USER_NOT_EXIST)
    if user.lover:
        lover = dict(
            username=user.lover.username,
            id=user.lover.id
        )
    else:
        lover = None

    result = dict(
        username=user.username,
        id=user.id,
        lover=lover
    )
    current_user.point = current_user.point - 1
    current_user.save()

    return response_json(data=result)
