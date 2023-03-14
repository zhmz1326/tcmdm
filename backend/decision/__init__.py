from flask import Blueprint

decision_blueprint = Blueprint('decision', __name__, url_prefix='/decision')
from . import api