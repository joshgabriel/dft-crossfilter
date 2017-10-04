from flask import Flask
from .tools.converters import ObjectIDConverter
from flask.ext.mongoengine import MongoEngine
#from flask_pymongo import PyMongo

db = MongoEngine()

#from pymongo import Connection
#connection = Connection()
#connection = Connection('localhost', 27017)
#db = connection

def setup_app(name,config='config'):
   app = Flask(name)
   app.config['MONGODB_SETTINGS'] = {
    'db': 'NIST_test',
    'host': 'localhost',
    'port': 27017
}
   db.init_app(app)
   app.url_map.converters['objectid'] = ObjectIDConverter
   app.debug = True
   return app


#def setup_app(name, config='config'):
#    app = Flask(__name__)
#    app.config["MONGO_DBNAME"] = "NIST_test"
#    global db
#    db = PyMongo(app, config_prefix='MONGO')
    #APP_URL = "http://127.0.0.1:5001"

    ## Original ##
    #app = Flask(name)
    #app.config.from_object(config)

#    app.debug = True

    # Flask-MongoEngine instance
#    db.init_app(app)

    # Custom Converters
#    app.url_map.converters['objectid'] = ObjectIDConverter

#    return app

#db,app = setup_app(__name__)
