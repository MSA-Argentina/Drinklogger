import datetime
from peewee import CharField, FloatField, TextField, IntegerField, \
    ForeignKeyField, DateField, BooleanField

from config import db

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
    password = CharField()

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
    activo = BooleanField(default=True)

    class Meta:
        order_by = ('-fecha',)
