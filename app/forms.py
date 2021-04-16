from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, widgets, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email



class RegistrationForm(FlaskForm):
    username = StringField(label='Nombre de Usuario', validators=[DataRequired(), Length (min=2, max=20)])
    password = StringField(label='Contraseña', validators=[DataRequired(), Length(min=6, max=16)])
    confirm_password = StringField(label='Repita la contraseña', validators=[DataRequired(), EqualTo('password')])
    email = StringField(label='Correo Electronico', validators=[DataRequired(), Email()])
    phone = StringField(label='Numero de Telefono Movil')
    Checkbox = BooleanField(label='Al seleccionar esta casilla esta indicando que ha leido y esta de acuerdo con los terminos y condiciones de One Stop Ride LLC.', validators=[DataRequired()])
    submit = SubmitField(label='Siguente')


class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired(), Length (min=2, max=20)])
    password = StringField(label='password', validators=[DataRequired(), Length(min=6, max=16)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    phone = StringField(label='Number Phone')
    submit = SubmitField(label='Login')