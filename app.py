from src.main.server.server import create_app
from src.databases.postgres.settings.postgres_config import PostgresDbAlchemy
from src.modules.catalog.models.catalog import Catalog
from src.modules.users.models.user import User
from src.databases.postgres.model.supplier import Supplier

app = create_app()
db = PostgresDbAlchemy.db


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(port=3000, debug=True, host='0.0.0.0')
