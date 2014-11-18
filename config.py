import logging
import os
from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.rest import RestAPI
from flask.ext.sendmail import Mail

# Configuracion
DATABASE = {
    'name': 'drinklogger',
    'engine': 'peewee.PostgresqlDatabase',
    'user': 'leandro',
    'password': '',
}

DEBUG = True # Activar fuera del repo
LOG_LEVEL = logging.DEBUG
SECRET_KEY = 'agfsdbdgbgfc' # Agregar fuera del repo
LOG_NAME = "drinklogger.log"

# Evita errores al traer templates en distintos ambientes
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'template')

app = Flask(__name__, template_folder=TEMPLATES_DIR)
app.config.from_object(__name__)
db = Database(app)
auth = Auth(app, db)
api = RestAPI(app)
mail = Mail(app)
