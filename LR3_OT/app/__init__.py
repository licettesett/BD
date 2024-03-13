from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)

login.login_view = 'login'
bootstrap = Bootstrap(app)

from app import views

