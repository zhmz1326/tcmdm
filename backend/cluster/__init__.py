from flask import Blueprint

cluster_blueprint = Blueprint('cluster', __name__, url_prefix='/cluster')
from . import api