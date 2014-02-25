import os
from flask import Flask
from flask_peewee.db import Database
from flask_peewee.auth import Auth

# Configuracion
DATABASE = {
    'name': 'drinklogger',
    'engine': 'peewee.PostgresqlDatabase',
    'user': 'leandro',
}

DEBUG = True
SECRET_KEY = '0303456'

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')

app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object(__name__)

db = Database(app)
auth = Auth(app, db)