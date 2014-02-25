import datetime
from config import app
from config import db
from peewee import *


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
    fecha = DateField(default=datetime.datetime.now().date())

    class Meta:
        order_by = ('-fecha',)
