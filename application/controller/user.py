from flask import jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from . import api
from ..model.user import User, Love
from ..helper import response_json
from config.status_code import *


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


@api.route('/logout', methods=['POST'])
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
        point=10
    )
    user.save()
    return response_json(data=dict(id=user.id))


@api.route('/love', methods=['POST'])
@login_required
def vindicate():
    sender_id = request.json.get('sender_id')
    receiver_id = request.json.get('receiver_id')
    if receiver_id:
        receiver = User.query.get(receiver_id)
        if not receiver:
            return response_json(LOVE_SENDER_NOT_EXIST)

        if len(current_user.send_love):
            return response_json(LOVE_SEND_EXIST)
        love = Love(
            from_id=current_user.id,
            to_id=receiver_id,
        )
    return jsonify(dict(key='This is love/post'))


@api.route('/love/<love_id>', methods=['GET'])
def accept(love_id):
    return jsonify(dict(key='This is love/get'))


@api.route('/notice', methods=['GET'])
def get_notice():
    return jsonify(dict(key='This is notice/get'))
