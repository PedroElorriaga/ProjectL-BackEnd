from src.main.server.server import create_app
from src.databases.postgres.settings.postgres_config import PostgresDbAlchemy
from src.databases.postgres.model.catalog import Catalog
from src.databases.postgres.model.user import User

app = create_app()
db = PostgresDbAlchemy.db

with app.app_context():
    db.create_all()

app.run(port=3000, debug=True, host='0.0.0.0')
