from flask import Flask
from flask_cors import CORS, cross_origin
from apriori import apriori_blueprint
from bk import bk_blueprint
from cluster import cluster_blueprint
from decision import decision_blueprint

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def hello_world():
    return 'Welcome, this is TCM Data Mining Project'

app.register_blueprint(apriori_blueprint)
app.register_blueprint(bk_blueprint)
app.register_blueprint(cluster_blueprint)
app.register_blueprint(decision_blueprint)

if __name__ == '__main__':
    app.run(port=2023, debug=True)
