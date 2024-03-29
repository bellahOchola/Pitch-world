from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask import Flask
from config import config_options
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail


mail = Mail()
csrf = CSRFProtect()
bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)

    # creating app configurations
    app.config.from_object(config_options[config_name])
    app.config['SECRET_KEY'] = 'snskdcjkl5jksclc9'

    # registering blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    return app