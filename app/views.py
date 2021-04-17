"""Defines the home page route"""
import sqlite3
import os
import bcrypt as Bcrypt
import base64

from flask import  (
    render_template,
    url_for,
    redirect,
    Blueprint,
    current_app, 
    flash,
    session,
    Flask,
    request as app
)
from flask import request
from .ds_config import DS_CONFIG
from .ds_config import EXAMPLES_API_TYPE
from .forms import RegistrationForm, LoginForm
#from .models import db
import pyodbc

core = Blueprint("core", __name__)

currentdirectory = os.path.join(os.path.dirname(__file__))

@core.route("/")
def index():
    return render_template("home.html", title="Home")



@core.route("/index")
def r_index():
    return redirect(url_for("core.index"))


@core.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@core.app_errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@core.route("/register", methods=('GET', 'POST'))
def register():



    form=RegistrationForm()
#    if form.validate_on_submit():
#        return redirect(url_for("core.index"))

    if request.method == 'POST':
        password = form.password.data
        encPass = password.encode("utf-8") #password.encode('utf-8') 
        if form.validate_on_submit():
            b64 = base64.b64encode(encPass)
            hashed_password = Bcrypt.hashpw(b64, Bcrypt.gensalt())
#            if Bcrypt.checkpw(b64, hashed_password): ESTE FRAGMENTO DE CODIGO ESTA SIENDO GUARDADO PARA LA AUTENTIFICACION DEL USUARIO OSEA LOGIN
#                print("It Matches!")
#            else:
#                print("It Does not Match :(")
            if hashed_password:
                try:
                    connection = sqlite3.connect(currentdirectory + "\database2.db")
                    cursor = connection.cursor()
                    cursor.execute("create table Drivers (lang_name, lang_email, lang_password, lang_phone)") #.format(data=data)
                except sqlite3.OperationalError:
                    print("la tabla ya existe {username}".format(username=form.username.data))

                target_fish_name = "jansgreen"                
                cursor.execute("INSERT INTO Drivers(lang_name, lang_email, lang_password, lang_phone) VALUES(?,?,?,?)", [(form.username.data), (form.email.data), (hashed_password), (form.phone.data), ])
                connection.commit()

                username = form.username.data
                email = form.email.data
                phone = form.phone.data


                lang_name = cursor.execute( "SELECT lang_name, lang_email, lang_phone FROM Drivers WHERE lang_name = ?",(username,),).fetchall()
                for user in lang_name:
                    print(user.count)
                username = user.split("() ")
                print(username)
                print('buscando el usuario')
                lang_email = cursor.execute( "SELECT lang_email FROM Drivers WHERE lang_email = ?",(email,),).fetchall()
                print(lang_email)
                print('buscando el email {lang_email}')

                lang_phone = cursor.execute( "SELECT lang_phone FROM Drivers WHERE lang_phone = ?",(phone,),).fetchall()
                print(lang_phone)
                print('buscando el phone {lang_phone}')

                if "Luis" == "Luis":
                    print('El usuario ya Existe')
                elif form.email.data == lang_email:
                    print('El Email ya esta registrado')
                elif form.phone.data == lang_phone:
                    print('El Email ya esta registrado')
                else:
                    print('no hay coincidencia')




                #user = User(username=form.username.data, password=hashed_password, email=form.email.data, phone=form.phone.data)
                #db.session.add(user)
                #db.session.commit
                #session.modified = True
                #cursor  =  cnxn . cursor ()
                rows = cursor.execute( "SELECT lang_email FROM Drivers WHERE lang_name = ?",(target_fish_name,),).fetchall()
                print(rows)
#                for row in cursor.execute('SELECT * FROM Drivers ORDER BY lang_name'):
#                    print(row)
                connection.close()

                return redirect(url_for('core.index'))
    

    return render_template('register.html', title='Register', form=form)