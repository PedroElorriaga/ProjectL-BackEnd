# Dev database with Docker Compose

This project uses PostgreSQL for development. Use Docker Compose so every developer starts with the same database service configuration.

## 1) Prepare environment

1. Copy `.env.example` to `.env` (if you do not have one yet).
2. Keep `SQLALCHEMY_DATABASE_URI` using `localhost` if your Flask app runs on host machine.

Example:

`SQLALCHEMY_DATABASE_URI=postgresql+psycopg://postgres:123456@localhost:5432/postgres`

## 2) Start database

From project root:

```bash
docker compose up -d db
```

Check status:

```bash
docker compose ps
docker compose logs -f db
```

## 3) Run migrations

After pulling new code or migration files:

```bash
alembic upgrade head
```

When you create schema changes:

```bash
alembic revision --autogenerate -m "describe_change"
alembic upgrade head
```

Commit migration files from `alembic/versions/` so other developers can run the same schema updates.

## 4) Stop / reset

Stop container:

```bash
docker compose stop db
```

Stop and remove container:

```bash
docker compose down
```

Remove container + volume (deletes all local DB data):

```bash
docker compose down -v
```

## 5) Auto-migration safety

Pytest now auto-upgrades migrations before every test run (fixture in `tests/conftest.py`).

If a teammate pulls new migrations and forgets to run `alembic upgrade head`, tests will apply them automatically.
This prevents "schema mismatch" errors during development.

**You'll see:**
- ✓ Database migrations applied successfully. (tests run normally)
- ✗ Migration failed: ... (tests fail, migrations blocked — fix and retry)

## Notes

- Compose synchronizes service configuration, not your local data.
- Schema consistency across developers comes from Alembic migration files committed to git.
- Every `pytest` run ensures the database schema is up-to-date.
