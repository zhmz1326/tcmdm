from flask import Blueprint

apriori_blueprint = Blueprint('apriori', __name__, url_prefix='/apriori')
from . import api