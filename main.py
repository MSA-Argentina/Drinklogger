# Imports
import datetime
from config import app
from config import db
from database import *
from admin import admin
from flask import abort
from flask import render_template
from flask import request


# Esto crea las vistas del admin tipo django
admin.setup()


@app.errorhandler(404)
def pagNoEncontrada(error):
    return render_template("error.html", error=error.code)


@app.errorhandler(406)
def pagErrorValores(error):
    return render_template("error.html", error=error.code)


@app.route("/")
def home():
    productos = Producto.select()
    usuarios = Usuario.select()
    exito = None
    semana_pasada = datetime.datetime.now() - datetime.timedelta(7)
    semana_pasada = semana_pasada.date()
    return render_template("index.html", productos=productos,
                           usuarios=usuarios, semana_pasada=semana_pasada,
                           exito=exito,)


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
                .where((Consumo.fecha >= pasado) & (Consumo.fecha <= futuro))
            # Mejorar este codigo
            for detalle in consumo_semanal:
                if str(detalle.usuario.nombre) not in arreglo_consumo:
                    arreglo_consumo[str(detalle.usuario.nombre)] \
                        = detalle.precio * detalle.cantidad
                else:
                    arreglo_consumo[str(detalle.usuario.nombre)] \
                        += detalle.precio * detalle.cantidad
            if (futuro == datetime.datetime.now().date()):
                return render_template("consultas.html",
                                       consumos=arreglo_consumo,
                                       pasado=str(pasado),
                                       futuro="hoy",)
            else:
                return render_template("consultas.html",
                                       consumos=arreglo_consumo,
                                       pasado=str(pasado),
                                       futuro=str(futuro),)
        else:
            abort(406)
    else:
        abort(406)


@app.route("/consulta/<usuario>/<pasado>-a-<futuro>/", methods=["GET"])
def consulta_detalle(usuario, pasado, futuro):
    if (usuario != '' and pasado != '' and futuro != ''):
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
        return render_template("detalle.html",
                               usuario=usuario,
                               detalles=usuario_detalle,)
    else:
        abort(406)


# Principal
if __name__ == '__main__':
    app.run()
