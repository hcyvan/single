from flask import Blueprint

api = Blueprint('api', __name__)

from .user import *
from .notice import *
