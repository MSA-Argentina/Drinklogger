# -*- coding: utf-8 -*-
# TODO: Reescribir
import datetime

from peewee import fn
from flask.ext.sendmail import Message
from jinja2 import Environment, FileSystemLoader

from database import Consumo, Usuario 
from application import mail

presente = datetime.datetime.now()
pasado = presente - datetime.timedelta(days=7)

try:
    consumo_semanal = (Consumo.select(
        Usuario.nombre,
        fn.sum(Consumo.precio*Consumo.cantidad).alias('total')
        ).join(Usuario
            ).where((Consumo.fecha >= pasado)
               & (Consumo.fecha <= presente)
               & (Consumo.activo == True))\
            .group_by(Usuario.id)\
            .order_by(Usuario.nombre.desc()))

    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('mail.html')
    cuerpo_mensaje = template.render(datos=consumo_semanal,
                        pasado=pasado,
                        presente=presente)

    confirmacion = Message("Reporte Semanal",
                            sender=("Sistema", "no-reply@bebidas.msa"),
                            recipients=['lpoblet@msa.com.ar'])
    confirmacion.html = cuerpo_mensaje
    mail.send(confirmacion)
    print 'Email enviado.'
except Exception as expt:
    raise expt

