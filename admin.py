from flask_peewee.admin import Admin, ModelAdmin
from flask_peewee.rest import RestResource

from application import app, auth, api
from database import Producto, Consumo


class ProductoAdmin(ModelAdmin):
    columns = ("nombre", "precio", "cant",)


class ConsumoAdmin(ModelAdmin):
    columns = ("producto", "usuario", "fecha",
               "cantidad", "precio", "activo",)
    filter_fields = ("fecha",)


class UsuarioAdmin(ModelAdmin):
    columns = ("nombre", "email",)

class ProductoResource(RestResource):
    exclude = ('desc',)


admin = Admin(app, auth, branding="Drinklogger")
admin.register(Producto, ProductoAdmin)
admin.register(Consumo, ConsumoAdmin)

api.register(Producto, ProductoResource)
