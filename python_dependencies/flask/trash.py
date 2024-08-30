from flask import Flask, render_template, url_for, redirect
from flask_login import  login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask_bcrypt import Bcrypt
from flask import send_from_directory
from user import User





app = Flask(__name__)
bcrypt = Bcrypt(app)
userdb = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=150)], render_kw={"placeholder": "Username or Email"})
    password = StringField(validators=[InputRequired(), Length(
        min=8, max=100)], render_kw={"placeholder": "Passowrd"})

    submit = SubmitField("Register")


@app.route("/")
def home():
    return render_template('main.html')


@app.route("/login",  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User()
    if user.validate_and_login(form):
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, email=form.email.data)
        userdb.session.add(new_user)
        userdb.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form, errors=form.errors)


@app.route("/dashboard",  methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('static/images', filename)


if __name__ == "__main__":
    with app.app_context():
        userdb.create_all()
    app.run(debug=True)
