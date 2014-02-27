from hashlib import md5
from config import app
from config import db
from config import auth
from database import *
from flask import request
from flask import redirect
from flask_peewee.admin import Admin
from flask_peewee.admin import AdminPanel
from flask_peewee.admin import ModelAdmin


class ProductoAdmin(ModelAdmin):
    columns = ("nombre", "precio", "cant",)


class ConsumoAdmin(ModelAdmin):
    columns = ("producto", "usuario", "fecha", "cantidad", "precio",)
    filter_fields = ("fecha",)

class UsuarioAdmin(ModelAdmin):
    columns = ("nombre", "email",)

class UsuarioPanel(AdminPanel):
    template_name = "admin/usuarios.html"

    def get_urls(self):
        return (
            ("/create/", self.create),
        )

    def create(self):
        if request.method == "POST":
            if ((request.form["nombre"] != "")\
                and (request.form["email"] != "")\
                and (request.form["pass"] != "")):
                Usuario.create(
                    nombre=str(request.form["nombre"]),
                    email=str(request.form["email"]),
                    password=md5(request.form["pass"]).hexdigest()
                )
            next = request.form.get("next") or self.dashboard_url()
            return redirect(next)

    def get_context(self):
        return {
            'usuarios': Usuario.select().order_by(Usuario.id.asc())
        }


admin = Admin(app, auth, branding="Drinklogger")
admin.register(Producto, ProductoAdmin)
admin.register_panel('Usuarios', UsuarioPanel)
admin.register(Consumo, ConsumoAdmin)
