from flask import jsonify
from . import api


@api.route('/login', methods=['POST'])
def login():
    return jsonify(dict(key='This is login'))


@api.route('/register', methods=['POST'])
def register():
    return jsonify(dict(key='This is register'))


@api.route('/love', methods=['POST'])
def vindicate():
    return jsonify(dict(key='This is love/post'))


@api.route('/love/<love_id>', methods=['GET'])
def accept(love_id):
    return jsonify(dict(key='This is love/get'))


@api.route('/notice', methods=['GET'])
def get_notice():
    return jsonify(dict(key='This is notice/get'))
