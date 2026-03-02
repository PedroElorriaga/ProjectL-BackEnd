import os
from flask import Flask
from src.modules.catalog.routes.catalog import catalog_route
from src.modules.login.routes.login import login_route
from src.main.routes.root import root_route
from src.modules.suppliers.routes.supplier import supplier_route
from src.modules.users.routes.user import user_route
from src.databases.postgres.settings.postgres_config import PostgresDbAlchemy
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()
BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..'))

db = PostgresDbAlchemy.db


def create_app() -> Flask:
    app = Flask(__name__, static_folder=os.path.join(
        BASE_DIR, 'static'), static_url_path='/static')

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CLOUDNARY_NAME'] = os.getenv('CLOUDNARY_NAME')
    app.config['CLOUDNARY_API_KEY'] = os.getenv('CLOUDNARY_API_KEY')
    app.config['CLOUDNARY_API_SECRET'] = os.getenv('CLOUDNARY_API_SECRET')

    db.init_app(app)

    # CATALOG REDIRECT
    app.register_blueprint(root_route, url_prefix='/')
    app.register_blueprint(catalog_route, url_prefix='/catalogo')
    app.register_blueprint(login_route, url_prefix='/login')
    app.register_blueprint(supplier_route, url_prefix='/fornecedor')
    app.register_blueprint(user_route, url_prefix='/usuario')

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    return app
