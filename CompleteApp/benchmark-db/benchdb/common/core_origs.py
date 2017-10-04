from flask import Flask
from .tools.converters import ObjectIDConverter
from flask.ext.mongoengine import MongoEngine
from flask_pymongo import PyMongo

## Original ##
#db = MongoEngine()

def setup_app(name, config='config'):
    app = Flask(__name__)
    app.config["MONGO_DBNAME"] = "NIST_test"
    db = PyMongo(app, config_prefix='MONGO')
    #APP_URL = "http://127.0.0.1:5001"

    ## Original ##
    #app = Flask(name)
    #app.config.from_object(config)

    app.debug = True

    # Flask-MongoEngine instance
    db.init_app(app)

    # Custom Converters
    app.url_map.converters['objectid'] = ObjectIDConverter

    return app
