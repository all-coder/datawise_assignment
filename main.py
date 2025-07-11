import os
import flask
import flask_cors
from routes.dataset_routes import dataset_route
from routes.qlogs_routes import qlog_routes
from flask import Blueprint
from utils.mongo_connect import get_db
from flasgger import Swagger
from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)
swagger = Swagger(app)
flask_cors.CORS(app)


MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017/")
db = get_db(MONGO_DB_URI)
app.config["db"] = db

api = Blueprint('api', __name__)
api.register_blueprint(dataset_route, url_prefix="/datasets")
api.register_blueprint(qlog_routes, url_prefix="/datasets")

app.register_blueprint(api, url_prefix="/api")

@app.route('/')
def index():
    return {"status": "running", "message": "Dataset API"}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
