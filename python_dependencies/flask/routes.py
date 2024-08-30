from flask import Blueprint, render_template, redirect, send_from_directory, url_for, Flask
from flask_login import login_user
from loginform import LoginForm  
from user import User, userdb, bcrypt
from registerform import RegisterForm
from flask_wtf import CSRFProtect


app = Flask(__name__)
routes = Blueprint('routes', __name__)
routes.static_folder = '/static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
userdb.init_app(app)
csrf = CSRFProtect(app)



@routes.route("/")
def home():
    return render_template('home.html')


@routes.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User()
    if user.validate_existent_user(form):
        return render_template('dashboard.html')
    return render_template('login.html', form = form)

@routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.register_user():
        return render_template('login.html', form = form)
    return render_template('register.html', form=form, errors=form.errors)


@routes.route("/logout")
def logout():
    form = LoginForm()
    return render_template('login.html', form = form)

@routes.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@routes.route('/static/<path:filename>')
def serve_css(filename):
    return send_from_directory('static/css', filename)


#static\images\favicon.ico