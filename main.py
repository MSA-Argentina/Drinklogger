#Imports
from flask import Flask
from flask import render_template
from peewee import *
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask_peewee.admin import ModelAdmin
from flask_peewee.rest import RestAPI
from flask_peewee.rest import RestResource
import os
import datetime
from flask_peewee.auth import Auth

#Configuracion
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
api = RestAPI(app)

# Modelos
class Producto(db.Model):
	nombre = CharField()
	desc = TextField()
	cant = IntegerField()

	class Meta:
		order_by = ('nombre',)

	def __unicode__(self):
		return self.nombre


class Usuario(db.Model):
	nombre = CharField()
	email = CharField()
	is_admin = BooleanField(default=False, null=True)

	class Meta:
		order_by = ('nombre',)

	def __unicode__(self):
		return self.nombre


class Consumo(db.Model):
	usuario = ForeignKeyField(Usuario)
	producto = ForeignKeyField(Producto)
	cantidad = IntegerField()
	fecha = DateTimeField(default=datetime.datetime.now)

	class Meta:
		order_by = ('fecha',)

	def __unicode__(self):
		return '%s: %s (%s)' % (self.usuario, self.producto, self.fecha)

#Admin
class ProductoAdmin(ModelAdmin):
	columns = ('nombre', 'cant',)


admin = Admin(app, auth)
admin.register(Producto, ProductoAdmin)
admin.register(Usuario)
admin.register(Consumo)

admin.setup()

#REST API
class ProductoConf(RestResource):
	exclude = ('id', 'desc',)

api.register(Producto)

api.setup()

#Vistas

@app.route("/")
def home():
	return render_template('index.html')

#Principal
if __name__ == '__main__':
	auth.User.create_table(fail_silently=True)
	Producto.create_table(fail_silently=True)
	Usuario.create_table(fail_silently=True)
	Consumo.create_table(fail_silently=True)

	app.run()