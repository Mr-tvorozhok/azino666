
from wtforms import StringField, SubmitField, TextAreaField,  BooleanField, PasswordField
from flask_wtf import FlaskForm
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    remember = BooleanField("Remember Me")
    submit = SubmitField()