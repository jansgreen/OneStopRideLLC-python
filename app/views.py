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
from .forms import RegistrationForm, LoginForm, registerInfoUserForm
#from .models import db

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
    if request.method == 'POST':
        password = form.password.data
        encPass = password.encode("utf-8")
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
                    cursor.execute("create table Users (lang_name, lang_email, lang_password, lang_phone)") #.format(data=data)
                except sqlite3.OperationalError:
                    flash("Ocurrio un error, por favor contacte a One Stop Ride LLC")

                username = form.username.data
                email = form.email.data
                phone = form.phone.data

                lang_name = cursor.execute( "SELECT lang_name, lang_email, lang_phone FROM Users WHERE lang_name = ?",(username,),).fetchone()
                if lang_name:
                    for user in lang_name:
                        if user == form.username.data:
                            flash('El usuario ya Existe')
                            return render_template('register.html', title='Register', form=form)
                        elif user == form.email.data:
                            flash('El Email ya esta registrado')
                            return render_template('register.html', title='Register', form=form)
                        elif user == form.phone.data:
                            flash('El Email ya esta registrado')
                            return render_template('register.html', title='Register', form=form)
                        else:
                            cursor.execute("INSERT INTO Users(lang_name, lang_email, lang_password, lang_phone) VALUES(?,?,?,?)", [(form.username.data), (form.email.data), (hashed_password), (form.phone.data), ])
                            connection.commit()
                            flash('Se ha creado el usuario')
                            connection.close()
                            return redirect(url_for('core.registerInfoUser', username=form.username.data))
                else:
                    cursor.execute("INSERT INTO Users(lang_name, lang_email, lang_password, lang_phone) VALUES(?,?,?,?)", [(form.username.data), (form.email.data), (hashed_password), (form.phone.data), ])
                    connection.commit()
                    flash('Se ha creado el usuario')
                    connection.close()
                    return redirect(url_for('core.registerInfoUser', username=form.username.data))
                        
                return redirect(url_for('core.index'))
    return render_template('register.html', title='Register', form=form)



# SEGUNDO PASO DE LA REGISTRACION INGRESANDO INFORMACION PERSONAL DEL USUARIO


@core.route("/registerInfoUser/<username>", methods=('GET', 'POST'))
def registerInfoUser(username):
    form=registerInfoUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            try:
                connection = sqlite3.connect(currentdirectory + "\database2.db")
                cursor = connection.cursor()
                cursor.execute("create table Perfil (PrimerNombre, SegunNombre, PrimerApellido, SegundoApellido, SSN, NumeroIdentidad, Direccion, Users text not null references Users(username))")

            except sqlite3.OperationalError:
                flash("Ocurrio un error, por favor contacte a One Stop Ride LLC")

            perfiles = cursor.execute( "SELECT PrimerNombre, SegunNombre, PrimerApellido, SegundoApellido, SSN, NumeroIdentidad, Direccion, Users FROM Perfil WHERE Users = ?",(username,),).fetchone()
            print(perfiles)
            print(username)
            print("Buscando si ya existe")
            print("======================================================")



            if perfiles: 
                for perfil in perfiles:
                    if perfil == form.PrimerNombre.data:
                        flash('El usuario ya Existe')
                        return render_template('register.html', title='Register', form=form)
                    elif perfil == form.SegunNombre.data:
                        flash('El Email ya esta registrado')
                        return render_template('register.html', title='Register', form=form)
                    elif perfil == form.PrimerApellido.data:
                        flash('El Email ya esta registrado')
                        return render_template('register.html', title='Register', form=form)
                    elif perfil == form.SegundoApellido.data:
                        flash('El usuario ya Existe')
                        return render_template('register.html', title='Register', form=form)
                    elif perfil == form.SSN.data:
                        flash('El Email ya esta registrado')
                        return render_template('register.html', title='Register', form=form)
                    elif perfil == form.NumeroIdentidad.data:
                        flash('El Email ya esta registrado')
                        return render_template('register.html', title='Register', form=form)
                    elif perfil == form.Direccion.data:
                        flash('El Email ya esta registrado')
                        return render_template('register.html', title='Register', form=form)
                    else:
                        cursor.execute("INSERT INTO Perfil(PrimerNombre, SegunNombre, PrimerApellido, SegundoApellido, SSN, NumeroIdentidad, Direccion, Users) VALUES(?,?,?,?,?,?,?,?)", [(form.PrimerNombre.data), (form.SegunNombre.data), (form.PrimerApellido.data), (form.SegundoApellido.data), (form.SSN.data), (form.NumeroIdentidad.data), (form.Direccion.data) (username)])
                        connection.commit()
                        flash('Se ha creado el usuario')
                        perfiles = cursor.execute( "SELECT PrimerNombre, SegunNombre, PrimerApellido, SegundoApellido, SSN, NumeroIdentidad, Direccion, Users FROM Perfil WHERE Users = ?",(username,),).fetchone()
                        print(perfiles)
                        connection.close()
            else:
                cursor.execute("INSERT INTO Perfil(PrimerNombre, SegunNombre, PrimerApellido, SegundoApellido, SSN, NumeroIdentidad, Direccion, Users) VALUES(?,?,?,?,?,?,?,?)", [(form.PrimerNombre.data), (form.SegunNombre.data), (form.PrimerApellido.data), (form.SegundoApellido.data), (form.SSN.data), (form.NumeroIdentidad.data), (form.Direccion.data), (username)])
                connection.commit()
                flash('Se ha creado el usuario')
                perfiles = cursor.execute( "SELECT PrimerNombre, SegunNombre, PrimerApellido, SegundoApellido, SSN, NumeroIdentidad, Direccion, Users FROM Perfil WHERE Users = ?",(username,),).fetchall()
                print(perfiles)
                print("imprimiendo una lista")
                print("======================================================")
                connection.close()
            return redirect(url_for('core.index'))
    return render_template('registerInfoUser.html', title='Register', form=form)