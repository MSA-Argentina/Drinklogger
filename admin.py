from config import app
from config import db
from config import auth
from database import *
from flask_peewee.admin import Admin
from flask_peewee.admin import ModelAdmin

class ProductoAdmin(ModelAdmin):
    columns = ("nombre", "precio", "cant",)


class ConsumoAdmin(ModelAdmin):
    columns = ("producto", "usuario", "fecha", "cantidad", "precio",)
    filter_fields = ("fecha",)


admin = Admin(app, auth, branding="Drinklogger")
admin.register(Producto, ProductoAdmin)
admin.register(Usuario)
admin.register(Consumo, ConsumoAdmin)