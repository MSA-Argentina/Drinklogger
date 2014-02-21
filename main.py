# Imports
import os
import datetime
from flask import Flask
from flask import render_template
from flask import request
from peewee import *
from flask_peewee.db import Database
from flask_peewee.admin import Admin
from flask_peewee.admin import ModelAdmin
from flask_peewee.rest import RestResource
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

# Modelos


class Producto(db.Model):
    nombre = CharField()
    precio = FloatField()
    desc = TextField()
    cant = IntegerField()

    class Meta:
        order_by = ('nombre',)

    def __unicode__(self):
        return self.nombre


class Usuario(db.Model):
    nombre = CharField()
    email = CharField()

    class Meta:
        order_by = ('nombre',)

    def __unicode__(self):
        return self.nombre


class Consumo(db.Model):
    usuario = ForeignKeyField(Usuario)
    producto = ForeignKeyField(Producto)
    precio = FloatField()
    cantidad = IntegerField()
    fecha = DateTimeField(default=datetime.datetime.now)

    class Meta:
        order_by = ('-fecha',)

    def __unicode__(self):
        return '%s: %s (%s)' % (self.usuario, self.producto, self.fecha)


# Admin
class ProductoAdmin(ModelAdmin):
    columns = ("nombre", "precio", "cant",)


class ConsumoAdmin(ModelAdmin):
    columns = ("producto", "usuario", "fecha", "cantidad",)
    filter_fields = ("fecha",)

admin = Admin(app, auth, branding="Drinklogger")
admin.register(Producto, ProductoAdmin)
admin.register(Usuario)
admin.register(Consumo, ConsumoAdmin)

admin.setup()

# Vistas


@app.route("/")
def home():
    productos = Producto.select()
    usuarios = Usuario.select()
    consumo = Consumo.select().limit(5)
    exito = None
    return render_template("index.html", productos=productos,
                           usuarios=usuarios, exito=exito,)


@app.route("/mandar", methods=["POST", "GET"])
def consumo():
    productos = Producto.select()
    usuarios = Usuario.select()
    consumo = Consumo.select()
    if (request.form["productos"] != "null"):
        cantidad_actual = Producto\
            .get(Producto.id == request.form["productos"]).cant
        if (request.form["cantidad"] > cantidad_actual):
            cantidad_nueva = cantidad_actual - int(request.form["cantidad"])
            consumo = Consumo()
            consumo.usuario = request.form["personas"]
            consumo.producto = request.form["productos"]
            consumo.precio = Producto.select()\
                .where(Producto.id == request.form["productos"]).get().precio
            consumo.cantidad = request.form["cantidad"]
            consumo.save()
            actualizar_cantidad = Producto.update(cant=cantidad_nueva)\
                .where(Producto.id == request.form["productos"])
            actualizar_cantidad.execute()
            exito = True
            return render_template("index.html", productos=productos,
                                   usuarios=usuarios, exito=exito,)
        else:
            exito = False
            return render_template("index.html", productos=productos,
                                   usuarios=usuarios, exito=exito,)
    else:
        exito = False
        return render_template("index.html", productos=productos,
                               usuarios=usuarios, exito=exito,)

@app.route("/consulta/", methods=["POST"])
def consulta():
    if (request.form["fecha"] != ""):
        import datetime
        ahora = str(datetime.datetime\
                .strftime(datetime.datetime.now(), "%Y-%m-%d"))
        fecha = str(datetime.datetime\
                .strptime(request.form["fecha"], "%Y-%m-%d").date())
        consumo_semanal = Consumo.select()\
            .where(Consumo.fecha == fecha)
        return render_template("consultas.html", consumo=consumo_semanal)

# Principal
if __name__ == '__main__':
    Usuario.create_table(fail_silently=True)
    Producto.create_table(fail_silently=True)
    Consumo.create_table(fail_silently=True)
    app.run()
