import config

from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.rest import RestAPI
from flask.ext.sendmail import Mail


app = Flask("drinklogger", template_folder=config.TEMPLATES_DIR)
app.config.from_object(config)

db = Database(app)
auth = Auth(app, db)
api = RestAPI(app)
mail = Mail(app)
