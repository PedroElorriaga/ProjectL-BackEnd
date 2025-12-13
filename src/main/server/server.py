from flask import Flask, request
from src.main.routes.catalog import catalog_route
from src.main.routes.login import login_route
from src.models.mysql.settings.mysql_model import db
import os
from dotenv import load_dotenv
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix


load_dotenv()
BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..'))


def create_app() -> Flask:
    app = Flask(__name__, static_folder=os.path.join(
        BASE_DIR, 'static'), static_url_path='/static')

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1,
                            x_proto=1, x_host=1, x_prefix=1)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.before_request
    def force_https():
        if app.env != 'development' and not request.is_secure:
            request.environ['wsgi.url_scheme'] = 'https'

    app.register_blueprint(catalog_route, url_prefix='/catalogo')
    app.register_blueprint(login_route, url_prefix='/login')

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    return app
