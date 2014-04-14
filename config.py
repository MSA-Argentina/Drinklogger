import os
from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth
from flask_peewee.rest import RestAPI

# Configuracion
DATABASE = {
    'name': '',
    'engine': '',
    'user': '',
}

DEBUG = False # Activar fuera del repo
SECRET_KEY = '' # Agregar fuera del repo

# Evita errores al traer templates en distintos ambientes
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')

app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object(__name__)

db = Database(app)
auth = Auth(app, db)
api = RestAPI(app)
