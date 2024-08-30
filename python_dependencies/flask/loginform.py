from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=150)], render_kw={"placeholder": "Username or Email"})
    password = StringField(validators=[InputRequired(), Length(
        min=8, max=100)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")