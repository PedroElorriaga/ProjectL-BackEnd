import pytest
from alembic.config import Config
from src.services.alembic_service.alembic_util import run_migrations


@pytest.fixture(scope='session', autouse=True)
def ensure_migrations():
    run_migrations()
