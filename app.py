from flask import Flask
from routes.auth import auth
from utils.db import db
from flask_login import LoginManager
from models.user import User
from extensions import bcrypt

app = Flask(__name__)

bcrypt.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:superpaloman+12@localhost/authdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisismysecretkey'

app.register_blueprint(auth)