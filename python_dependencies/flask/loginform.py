from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, DateField
from wtforms.validators import InputRequired, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=150)], render_kw={"placeholder": "Username or Email"})
    password = StringField(validators=[InputRequired(), Length(
        min=8, max=100)], render_kw={"placeholder": "Passowrd"})

    submit = SubmitField("Register")