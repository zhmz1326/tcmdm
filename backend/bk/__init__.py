from flask import Blueprint

bk_blueprint = Blueprint('bk', __name__, url_prefix='/bk')
from . import api