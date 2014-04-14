# -*- coding: utf-8 -*-
# Imports
import datetime
from hashlib import md5
from config import app
from config import db
from config import api
from config import auth
from database import *
from admin import admin
from flask import abort
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for


# Esto crea las vistas del admin tipo django
admin.setup()
# Y esto el API REST para el log de bebidas
api.setup()

# Errores genéricos
@app.errorhandler(404)
def pagNoEncontrada(error):
    args = {}
    args['error'] = error.code
    return render_template("error.html", args=args,)


@app.errorhandler(406)
def pagErrorValores(error):
    args = {}
    args['error'] = error.code
    return render_template("error.html", args=args,)

@app.route("/")
def home():
    productos = Producto.select()
    usuarios = Usuario.select()
    exito = None
    admin = auth.get_logged_in_user()
    semana_pasada = datetime.datetime.now() - datetime.timedelta(7)
    semana_pasada = semana_pasada.date()

    args = {}
    args['productos'] = productos
    args['usuarios'] = usuarios
    args['exito'] = None
    args['auth'] = admin
    args['semana_pasada'] = semana_pasada

    return render_template("index.html", args=args,)


@app.route("/mandar", methods=["POST", "GET"])
def consumo():
    usuarios = Usuario.select()
    consumo = Consumo.select()
    productos = Producto.select()
    admin = auth.get_logged_in_user()
    semana_pasada = datetime.datetime.now() - datetime.timedelta(7)
    semana_pasada = semana_pasada.date()
    get_usuario = Usuario.get(Usuario.id == request.form["personas"]).nombre
    get_pass = Usuario.get(Usuario.id == request.form["personas"]).password
    if (get_pass == md5(request.form["pass"].encode("utf-8")).hexdigest()):
        if (request.form["productos"] != "null"):
            cantidad_actual = Producto\
                .get(Producto.id == request.form["productos"]).cant
            if (request.form["cantidad"] > cantidad_actual):
                cantidad_nueva = cantidad_actual - \
                    int(request.form["cantidad"])
                consumo = Consumo()
                consumo.usuario = request.form["personas"]
                consumo.producto = request.form["productos"]
                consumo.precio = Producto.select()\
                    .where(Producto.id == request.form["productos"])\
                    .get().precio
                consumo.cantidad = request.form["cantidad"]
                consumo.save()
                actualizar_cantidad = Producto.update(cant=cantidad_nueva)\
                    .where(Producto.id == request.form["productos"])
                actualizar_cantidad.execute()
                exito = True
                error = None
            else:
                exito = False
                error = 'cantidad'        
        else:
            exito = False
            error = 'stock'
    else:
        exito = False
        error = 'pass'

    if (exito):
        return redirect(url_for('home'))
    else:
        args = {}
        args['error'] = error
        return render_template('error.html', args=args)


@app.route("/consulta/", methods=["POST"])
def consulta():
    admin = auth.get_logged_in_user()
    if (request.form["pasado"] != ""):
        from datetime import date
        anio, mes, dia = request.form["pasado"].split("-")
        pasado = date(int(anio), int(mes), int(dia))
        if (request.form["futuro"] == ""):
            futuro = datetime.datetime.now().date()
        else:
            anio, mes, dia = request.form["futuro"].split("-")
            futuro = date(int(anio), int(mes), int(dia))
        if (pasado <= futuro):
            arreglo_consumo = {}
            consumo_semanal = Consumo.select(Consumo.precio,
                                             Consumo.cantidad,
                                             Consumo.usuario,)\
                .where((Consumo.fecha >= pasado)
                       & (Consumo.fecha <= futuro)
                       & (Consumo.activo == True))
            # Mejorar este código
            for detalle in consumo_semanal:
                if str(detalle.usuario.nombre) not in arreglo_consumo:
                    arreglo_consumo[str(detalle.usuario.nombre)] \
                        = detalle.precio * detalle.cantidad
                else:
                    arreglo_consumo[str(detalle.usuario.nombre)] \
                        += detalle.precio * detalle.cantidad
            args = {}
            args['consumos'] = arreglo_consumo
            args['auth'] = admin
            args['pasado'] = str(pasado)
            args['futuro'] = str(futuro)
            return render_template("consultas.html", args=args,)
        else:
            abort(406)
    else:
        abort(406)


@app.route("/consulta/<usuario>/<pasado>-a-<futuro>/", methods=["GET"])
def consulta_detalle(usuario, pasado, futuro):
    if (usuario != "" and pasado != "" and futuro != ""):
        usuario_id = Usuario.get(Usuario.nombre == usuario).id
        usuario_detalle = Consumo.select(Consumo.producto,
                                         fn.Sum(Consumo.cantidad)
                                         .alias("cantidad"),
                                         Consumo.precio,
                                         Consumo.fecha)\
                                 .where((Consumo.usuario == usuario_id)
                                        & (Consumo.fecha >= pasado)
                                        & (Consumo.fecha <= futuro))\
                                 .group_by(Consumo.producto,
                                           Consumo.cantidad,
                                           Consumo.precio,
                                           Consumo.fecha)\
                                 .order_by(Consumo.fecha.asc())
        args = {}
        args['usuario'] = usuario
        args['detalles'] = usuario_detalle
        return render_template("detalle.html", args=args,)
    else:
        abort(406)


@app.route("/consulta/cierre/<pasado>-a-<futuro>/", methods=["GET"])
def cierre_consumos(pasado, futuro):
    if (pasado != "" and futuro != ""):
        productos = Producto.select()
        usuarios = Usuario.select()
        semana_pasada = datetime.datetime.now() - datetime.timedelta(7)
        semana_pasada = semana_pasada.date()

        cierre_usuario = Consumo.update(activo=False)\
            .where((Consumo.fecha >= pasado)
                   & (Consumo.fecha <= futuro))
        cierre_usuario.execute()

        args = {}
        args['productos'] = productos
        args['usuarios'] = usuarios
        args['exito'] = "Cierre"
        args['semana_pasada'] = semana_pasada

        return render_template("index.html", args=args,)


@app.route("/usuario/")
@auth.login_required
def manejo_usuario():
    user = auth.get_logged_in_user()
    usuarios = Usuario.select().order_by(Usuario.id.asc())
    return render_template("usuarios.html", usuarios=usuarios)


@app.route("/usuario/crear/", methods=["POST"])
def crear_usuario():
    if (request.form["nombre"] != "" \
        and request.form["email"] != ""\
        and request.form["pass"] != ""):
        try:
            Usuario.get(Usuario.email == request.form["email"])
            return redirect(url_for("manejo_usuario"))
        except Usuario.DoesNotExist:
            Usuario.create(
                nombre=request.form["nombre"],
                email=request.form["email"],
                password=md5(request.form["pass"]\
                         .encode("utf-8")).hexdigest(),
            )
            return redirect(url_for("manejo_usuario"))


@app.route("/usuario/editar/<id_usuario>/", methods=["GET"])
def editar_usuario(id_usuario):
    if (id_usuario != "" and id_usuario.isdigit()):
        usuario_datos = Usuario.get(Usuario.id == id_usuario)
        return render_template("editar.html", usuario=usuario_datos)
    else:
        abort(406)

@app.route("/usuario/editado/", methods=["POST"])
def edito_usuario():
    if request.method == "POST":
        datos_usuario = Usuario.get(Usuario.id == request.form["usuario_id"])
        if request.form["pass"] == "":
            act_usuario = Usuario.update(nombre=request.form["nombre"],
                                   email=request.form["email"],)\
                               .where(Usuario.id == request.form["usuario_id"])
            act_usuario.execute()
        else:
            passwd = md5(request.form["pass"].encode("utf-8")).hexdigest()
            passwd2 = md5(request.form["pass2"].encode("utf-8")).hexdigest()
            if (passwd == passwd2):
                act_usuario = Usuario.update(nombre=request.form["nombre"],
                                       email=request.form["email"],
                                       password=passwd,)\
                                   .where(Usuario.id == request.form["usuario_id"])
                act_usuario.execute()
        return redirect(url_for("manejo_usuario"))


@app.route("/usuario/eliminar/<usuario_id>/", methods=["GET"])
def elimino_usuario(usuario_id):
    if (usuario_id != "" and usuario_id.isdigit()):
        usuario_eliminar = Usuario.get(Usuario.id == usuario_id)
        usuario_eliminar.delete_instance()
        return redirect(url_for("manejo_usuario"))


# Principal
if __name__ == "__main__":
    # Crea las tablas pero no avisa si falló
    # Conviene borrar una vez hecha la primera pasada
    Usuario.create_table(fail_silently=True)
    Producto.create_table(fail_silently=True)
    Consumo.create_table(fail_silently=True)
    app.run()
