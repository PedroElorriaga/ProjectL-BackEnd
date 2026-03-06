import os
import sys
from alembic.config import Config
from alembic import command


def run_migrations():
    """Run Alembic migrations programmatically on Render."""
    # 1. Get absolute path to your project root (where alembic.ini is)
    # This goes up 3 levels from src/services/alembic_service/
    base_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..', '..'))
    ini_path = os.path.join(base_dir, 'alembic.ini')

    print(f"DEBUG: Initializing migrations from: {ini_path}")

    # 2. Load the Alembic config
    alembic_cfg = Config(ini_path)

    # 3. Explicitly set the folder where your 'versions' are
    # This ensures Alembic doesn't look in a relative 'alembic/' folder that might not exist
    alembic_cfg.set_main_option(
        'script_location', os.path.join(base_dir, 'alembic'))

    # 4. Get your database URL from Render Environment Variables
    # Using postgresql+psycopg:// is correct for SQLAlchemy 2.0
    db_url = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')

    if db_url:
        # If Render gives you 'postgres://', fix it to 'postgresql://'
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        # Set the URL in the Alembic config
        alembic_cfg.set_main_option('sqlalchemy.url', db_url)
        print("DEBUG: Database connection string loaded.")
    else:
        print("ERROR: No database URL found in environment variables!")
        return

    try:
        print("DEBUG: Running 'alembic upgrade head'...")
        command.upgrade(alembic_cfg, 'head')
        print("✓ SUCCESS: Database migrations applied successfully.")
    except Exception as e:
        print(f"✗ CRITICAL ERROR during migration: {e}")
        # On Render, if migrations fail, we should probably stop the app
        # sys.exit(1) # Uncomment this if you want to block the app from starting on failure
