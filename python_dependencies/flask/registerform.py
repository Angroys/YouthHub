from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField
from wtforms.validators import InputRequired, Length, ValidationError
from user import User, userdb, bcrypt



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=8, max=100)], render_kw={"placeholder": "Password"})
    email = EmailField(validators=[InputRequired(), Length(
        min=4, max=150)], render_kw={"placeholder": "Email"})
    birthday = DateField(validators=[InputRequired()], render_kw={
                         "placeholder": "Birthday"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(
            username=username.data).first()
        if existing_username:
            raise ValidationError('The username already exists')

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('The email already exists')
    def register_user(form):
        print("Form submitted!")
        if form.validate_on_submit():
            print("Form is valid!")
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data,
                            password=hashed_password, email=form.email.data)
            userdb.session.add(new_user)
            userdb.session.commit()
            

            print("User added to database!")
            return True
        print(form.errors)  
        return False
