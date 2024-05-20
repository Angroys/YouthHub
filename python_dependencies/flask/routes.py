from flask import Blueprint, render_template, redirect, url_for
from forms import LoginForm  # Ensure you have a LoginForm defined
from youthhubuser import User

routes = Blueprint('routes', __name__)

@routes.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User()
    if user.validate_and_login(form):
        return redirect(url_for('routes.dashboard'))
    return render_template('login.html', form=form)

@routes.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
