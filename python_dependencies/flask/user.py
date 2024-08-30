from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user
from flask_bcrypt import Bcrypt

userdb = SQLAlchemy()
bcrypt = Bcrypt()

class User(userdb.Model ,  UserMixin):
    id = userdb.Column(userdb.Integer, primary_key=True)
    username = userdb.Column(userdb.String(20), unique=True, nullable=False)
    password = userdb.Column(userdb.String(100), nullable=False)
    email = userdb.Column(userdb.String(150), nullable=False)
    
    def validate_existent_user(self, form):
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return True
            return False
    

