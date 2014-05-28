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
from flask import jsonify

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask
from flask import jsonify

def py_mail(SUBJECT, BODY, TO, FROM):
    #With this function we send out our html email
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
    Su aplicacion de correo no soporta el formato del reporte.
    Visitar el siguiente link <a href="#">online</a>!"""

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')

    MESSAGE.attach(HTML_BODY)
    server = smtplib.SMTP('smtp.gmail.com:587')

    # Print debugging output when testing
    #if __name__ == "__main__":
    #    server.set_debuglevel(1)

    # Credentials (if needed) for sending the mail
    password = "Peudguv8"

    server.starttls()
    server.login(FROM,password)
    server.sendmail(FROM, [TO], MESSAGE.as_string())
    server.quit()

if __name__ == "__main__":
    consumo_semanal = (Consumo.select(
        Usuario.nombre,
        fn.sum(Consumo.precio*Consumo.cantidad).alias('total')
        ).join(Usuario
            ).where(
                Consumo.activo == True).group_by(Usuario.id).order_by(Usuario.nombre.asc()))

    html_row = ""
    for consumo_item in consumo_semanal:
        html_row = html_row + """
            <tr>
                <td mc:edit="subtitle2" style="color: #a4a4a4; line-height: 25px; font-size: 12px; font-weight: normal; font-family: Helvetica, Arial, sans-serif;">
                    """+ str(consumo_item.usuario.nombre).title() + """
                </td>
                <td mc:edit="subtitle2" style="color: #a4a4a4; line-height: 25px; font-size: 12px; font-weight: normal; font-family: Helvetica, Arial, sans-serif;">
                    $""" + str(consumo_item.total).zfill(2)  + """
                </td>
            </tr>"""
        #print str(consumo_item.usuario.nombre).title() + '' +  str(consumo_item.total).zfill(2) 


    email_content = """
    <!DOCTYPE HTML>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0;">
        <style type="text/css">
            body{
                width: 100%; 
                background-color: #4c4e4e; 
                margin:0; 
                padding:0; 
                -webkit-font-smoothing: antialiased;
            }
            p,h1,h2,h3,h4{
                margin-top:0;
                margin-bottom:0;
                padding-top:0;
                padding-bottom:0;
            }
            html{
                width: 100%; 
            }
            
            table{
                font-size: 14px;
                border: 0;
            }
            
            /* ----------- responsivity ----------- */
            @media only screen and (max-width: 640px){
                /*------ top header ------ */
                .header-bg{width: 440px !important; height: 10px !important;}
                .main-header{line-height: 28px !important;}
                .main-subheader{line-height: 28px !important;}
                
                .container{width: 440px !important;}
                .container-middle{width: 420px !important;}
                .mainContent{width: 400px !important;}
                
                .main-image{width: 400px !important; height: auto !important;}
                .banner{width: 400px !important; height: auto !important;}
                /*------ sections ---------*/
                .section-item{width: 400px !important;}
                .section-img{width: 400px !important; height: auto !important;}
                /*------- prefooter ------*/
                .prefooter-header{padding: 0 10px !important; line-height: 24px !important;}
                .prefooter-subheader{padding: 0 10px !important; line-height: 24px !important;}
                /*------- footer ------*/
                .top-bottom-bg{width: 420px !important; height: auto !important;}
                
            }
            
            @media only screen and (max-width: 479px){
            
                /*------ top header ------ */
                .header-bg{width: 280px !important; height: 10px !important;}
                .top-header-left{width: 260px !important; text-align: center !important;}
                .top-header-right{width: 260px !important;}
                .main-header{line-height: 28px !important; text-align: center !important;}
                .main-subheader{line-height: 28px !important; text-align: center !important;}
                
                /*------- header ----------*/
                .logo{width: 260px !important;}
                .nav{width: 260px !important;}
                
                .container{width: 280px !important;}
                .container-middle{width: 260px !important;}
                .mainContent{width: 240px !important;}
                
                .main-image{width: 240px !important; height: auto !important;}
                .banner{width: 240px !important; height: auto !important;}
                /*------ sections ---------*/
                .section-item{width: 240px !important;}
                .section-img{width: 240px !important; height: auto !important;}
                /*------- prefooter ------*/
                .prefooter-header{padding: 0 10px !important;line-height: 28px !important;}
                .prefooter-subheader{padding: 0 10px !important; line-height: 28px !important;}
                /*------- footer ------*/
                .top-bottom-bg{width: 260px !important; height: auto !important;}
            }
        </style>
    </head>
      <body>
        <table border="0" width="100%" cellpadding="0" cellspacing="0">
            <tr bgcolor="#4c4e4e"><td height="30"></td></tr>
            <tr bgcolor="#4c4e4e">
                <td width="100%" align="center" valign="top" bgcolor="#4c4e4e">
                    <!---------   top header   ------------>
                    <table border="0" width="600" cellpadding="0" cellspacing="0" align="center" class="container">
                        <tr>
                            <td><img style="display: block;" src="http://promailthemes.com/campaigner/layout1/white/blue/img/top-header-bg.png" width="600" height="10" alt="" class="header-bg" /></td>
                        </tr>
                        <tr bgcolor="2780cb"><td height="5"></td></tr>
                        <tr bgcolor="2780cb">
                            <td align="center">
                                <table border="0" width="560" align="center" cellpadding="0" cellspacing="0" class="container-middle">
                                    <tr>
                                        <td>
                                            <table border="0" align="left" cellpadding="0" cellspacing="0" class="top-header-left">
                                                <tr>
                                                    <td align="center">
                                                        <table border="0" cellpadding="0" cellspacing="0" class="date">
                                                            <tr>
                                                                <td>
                                                                    <img editable="true" mc:edit="icon1" width="13" height="13" style="display: block;" src="http://promailthemes.com/campaigner/layout1/white/blue/img/icon-cal.png" alt="icon 1" />
                                                                </td>
                                                                <td>&nbsp;&nbsp;</td>
                                                                <td mc:edit="date" style="color: #fefefe; font-size: 11px; font-weight: normal; font-family: Helvetica, Arial, sans-serif;">
                                                                 """ + datetime.date.today().strftime("%A") + """ """ + datetime.date.today().strftime("%d") +""" """+ datetime.date.today().strftime("%B") + """
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </table>
                                            <table border="0" align="left" cellpadding="0" cellspacing="0" align="center" class="top-header-right">
                                                <tr><td width="30" height="20"></td></tr>
                                            </table>
                                            
                                            <table border="0" align="right" cellpadding="0" cellspacing="0" align="center" class="top-header-right">
                                                <tr>
                                                    <td align="center">
                                                        <table border="0" cellpadding="0" cellspacing="0" align="center" class="tel">
                                                            <tr>
                                                                <td>                                                                </td>
                                                                <td>&nbsp;&nbsp;</td>
                                                                <td mc:edit="tel" style="color: #fefefe; font-size: 11px; font-weight: normal; font-family: Helvetica, Arial, sans-serif;">
                                                                    MSA - DrinkLogger Reporte
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>
                                                </tr>                                           
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                    <table width="600" border="0" cellpadding="0" cellspacing="0" align="center" class="container" bgcolor="ececec">
                        <tr mc:repeatable><td height="35"></td></tr>
                        <!--------- section 1 --------->
                        <tr mc:repeatable>
                            <td>
                                <table border="0" width="560" align="center" cellpadding="0" cellspacing="0" class="container-middle">
                                    <tr><td align="center"><img style="display: block;" width="560" height="6" src="http://promailthemes.com/campaigner/layout1/white/blue/img/top-rounded-bg.png" alt="" class="top-bottom-bg" /></td></tr>
                                    <tr bgcolor="ffffff">
                                        <td>
                                            <table width="528" border="0" align="center" cellpadding="0" cellspacing="0" class="mainContent">
                                                <tr><td height="20"></td></tr>
                                                <tr>
                                                    <td>
                                                        <table border="0" align="left" cellpadding="0" cellspacing="0">
                                                            <tr><td height="30" width="30"></td></tr>
                                                        </table>
                                                        <table border="0" width="360" align="left" cellpadding="0" cellspacing="0" class="section-item">
                                                            <tr>
                                                                <td mc:edit="title2" style="color: #484848; font-size: 16px; font-weight: normal; font-family: Helvetica, Arial, sans-serif;">
                                                                    Nombre Usuario
                                                                </td>
                                                                <td mc:edit="title2" style="color: #484848; font-size: 16px; font-weight: normal; font-family: Helvetica, Arial, sans-serif;">
                                                                    Total
                                                                </td>
                                                            </tr>
                                                            <tr><td height="15" colspan="2"></td></tr>
                                                            """ + html_row + """
                                                        </table>
                                                    </td>
                                                </tr>
                                                <tr><td height="20"></td></tr>
                                            </table>
                                        </td>
                                    </tr>
                                    <tr><td align="center"><img style="display: block;" width="560" height="6" src="http://promailthemes.com/campaigner/layout1/white/blue/img/bottom-rounded-bg.png" alt="" class="top-bottom-bg" /></td></tr>
                                </table>
                            </td>
                        </tr><!--------- end section 1 --------->
                        <tr mc:repeatable><td height="35"></td></tr>
                    </table>
                    <table border="0" width="600" cellpadding="0" cellspacing="0" align="center" class="container">
                        <tr bgcolor="2780cb"><td height="14"></td></tr>
                        <tr bgcolor="2780cb">
                            <td mc:edit="copy3" align="center">
                                <a href="#" style="color: #ffffff; font-size: 16px; font-weight: normal; font-family: Helvetica, Arial, sans-serif;">DrinkLogger Admin</a>
                            </td>
                        </tr>
                        <tr>
                            <td><img style="display: block;" src="http://promailthemes.com/campaigner/layout1/white/blue/img/bottom-footer-bg.png" width="600" height="10" alt="" class="header-bg" /></td>
                        </tr>
                    </table>
                </td>
            </tr>
            <tr bgcolor="#4c4e4e"><td height="30"></td></tr>
        </table>
      </body>
    </html>
    """
    TO = 'stock@msa.com.ar'
    FROM ='reportes@msa.com.ar' 
    try:
        py_mail('DrinkLogger - Reporte Consumos', email_content, TO, FROM)
        print ("Email enviado")
    except Exception:
        print ("Email okay")
