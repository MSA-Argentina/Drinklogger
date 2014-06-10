import logging
import os


# Configuracion
DATABASE = {
    'name': 'drinklogger',
    'engine': 'peewee.PostgresqlDatabase',
    'user': 'felipe',
    'password': '',
}

DEBUG = True # Activar fuera del repo
LOG_LEVEL = logging.DEBUG
SECRET_KEY = 'change me' # Agregar fuera del repo
LOG_NAME = "drinklogger.log"

# Evita errores al traer templates en distintos ambientes
TEMPLATES_DIR= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template')

try:
    import config_local
except ImportError:
    pass
