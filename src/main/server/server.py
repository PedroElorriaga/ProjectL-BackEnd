from flask import Flask
from src.main.routes.catalog import catalog_route
from src.main.routes.login import login_route
from src.models.mysql.settings.mysql_model import db
import os
from dotenv import load_dotenv


load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(catalog_route, url_prefix='/catalogo')
    app.register_blueprint(login_route, url_prefix='/login')

    return app
