import pytest
import os
from alembic.config import Config
from alembic import command
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def ensure_migrations():
    """Auto-run Alembic upgrade before any tests run.

    This ensures the database schema matches the latest migration file,
    catching schema mismatches early in local dev or CI.
    """
    load_dotenv()

    alembic_cfg = Config(os.path.join(
        os.path.dirname(__file__), '..', 'alembic.ini'))

    # Read database URL from environment (set by .env or alembic/env.py)
    db_url = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
    if db_url:
        alembic_cfg.set_main_option('sqlalchemy.url', db_url)

    try:
        command.upgrade(alembic_cfg, 'head')
        print("\n✓ Database migrations applied successfully.")
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        print("  → Check your database connection and migration files.")
        raise
