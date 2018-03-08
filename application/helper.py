from http import HTTPStatus
from functools import partial
from flask import jsonify, current_app

from config import status_code
from config.status_code import *


def get_msg_by_code(code):
    def get_key_from_value(status_map, value):
        for k, v in status_map.items():
            if v == value:
                return k
        return ''

    msg = get_key_from_value(status_code.__dict__, code)
    return msg


def response_json(code=SUCCESS, data=None, msg=None, status=None):
    response = dict(code=code)
    if data is not None:
        response['data'] = data
    if not msg and current_app.config.get('DEBUG'):
        msg = get_msg_by_code(code)
    if msg is not None:
        response['msg'] = msg

    if status is None:
        if code == SUCCESS:
            status = HTTPStatus.OK
        elif code == NOT_LOGIN:
            status = HTTPStatus.UNAUTHORIZED
        else:
            status = HTTPStatus.BAD_REQUEST

    return jsonify(response), status


def parse_model_list(models):
    model_list = []
    for model in models:
        model_list.append(model.to_dict())

    return model_list


def parse_paginate(paginate):
    models = paginate.items
    model_list = parse_model_list(models)
    result = {
        'items': model_list,
        'pages': paginate.pages,
        'page_index': paginate.page,
        'page_size': paginate.per_page,
        'total': paginate.total,
    }

    return result
