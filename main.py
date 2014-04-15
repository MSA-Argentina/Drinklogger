# -*- coding: utf-8 -*-
# Imports
import datetime
import logging
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


logging.basicConfig(filename='drinklogger.log', level=logging.INFO)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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

@app.route("/", methods=["GET"])
@app.route("/?exito=<exito>", methods=["GET"])
@app.route("/?exito=<exito>&error=<error>", methods=["GET"])
def home(exito=None, error=None):
    productos = Producto.select()
    usuarios = Usuario.select()
    admin = auth.get_logged_in_user()
    semana_pasada = datetime.datetime.now() - datetime.timedelta(7)
    semana_pasada = semana_pasada.date()

    args = {}
    args['productos'] = productos
    args['usuarios'] = usuarios
    if request.method == 'GET':
        args['exito'] = request.args.get('exito')
    if (args['exito'] == None):
        args['error'] = None
    else:
        args['error'] = request.args.get('error')
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
            if (request.form["cantidad"] < cantidad_actual):
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
                logging.info('Compra exitosa: Usuario: %s - Producto: %s - Cantidad: %s - Fecha: %s' % (get_usuario,
                                                 request.form['productos'],
                                                 request.form['cantidad'],
                                                 datetime.datetime.now()))
            else:
                exito = False
                error = 'cantidad'
                logging.warning('Error de cantidad: Usuario %s' % (get_usuario.encode('utf-8')))
        else:
            exito = False
            error = 'stock'
            logging.warning('Error de stock: Usuario %s' % (get_usuario.encode('utf-8')))
    else:
        exito = False
        error = 'pass'
        logging.warning('Error de contraseña: Usuario: %s' % (get_usuario.encode('utf-8')))

    # Si es exitoso, te redirije al inicio
    if (exito):
        return redirect('?exito=%s' % exito)
    # Sino, devuelve un error
    else:
        return redirect('?exito=%s&error=%s' % (exito, error))

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
        usuario_detalle = Consumo.select()\
                                 .where((Consumo.usuario == usuario_id)
                                        & (Consumo.fecha >= pasado)
                                        & (Consumo.fecha <= futuro))\
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

        logging.info('Cierre de Caja: De %s a %s - Fecha: %s' % (pasado,
                                         futuro,
                                         datetime.datetime.now()))

        return redirect('/?exito=True')


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
            logging.info('Creación de Usuario: Nombre: %s - Fecha: %s' % (
                                             request.form['nombre']\
                                             .encode('utf-8'),
                                             datetime.datetime.now()))
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
        logging.info('Edición de Usuario: Id de usuario: %s - Fecha: %s' % (
                                         request.form["usuario_id"]\
                                         .encode('utf-8'),
                                         datetime.datetime.now()))
        return redirect(url_for("manejo_usuario"))


@app.route("/usuario/eliminar/<usuario_id>/", methods=["GET"])
def elimino_usuario(usuario_id):
    if (usuario_id != "" and usuario_id.isdigit()):
        usuario_eliminar = Usuario.get(Usuario.id == usuario_id)
        usuario_eliminar.delete_instance()
        logging.info('Eliminación de Usuario: Id de usuario: %s - Fecha: %s' % (
                                         usuario_id.encode('utf-8'),
                                         datetime.datetime.now()))
        return redirect(url_for("manejo_usuario"))


# Principal
if __name__ == "__main__":
    # Crea las tablas pero no avisa si falló
    # Conviene borrar una vez hecha la primera pasada
    Usuario.create_table(fail_silently=True)
    Producto.create_table(fail_silently=True)
    Consumo.create_table(fail_silently=True)
    app.run()
