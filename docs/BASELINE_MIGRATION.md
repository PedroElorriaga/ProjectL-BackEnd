# Baseline Migration for CI Testing

## Overview

This document explains the baseline migration setup created to support CI/CD testing in GitHub Actions and other continuous integration environments.

## The Problem

In CI environments, the database starts completely empty. The migration chain must create all tables from scratch. However, if early migrations try to alter or reference tables that don't exist yet, the migrations fail with errors like:

```
sqlalchemy.exc.ProgrammingError: (psycopg.errors.UndefinedTable) 
relation "supplier" does not exist
[SQL: ALTER TABLE supplier ALTER COLUMN numero_tel TYPE VARCHAR(20)]
```

This happens because:
- Migration `c179efb24a95` tries to alter the `supplier` table
- But in a fresh database, the `supplier` table was never created
- The migration chain has no starting point that creates the original schema

## The Solution: Baseline Migration

We created migration `1c9028d7e8d1_baseline_schema.py` as a **baseline** that:

1. **Sets `down_revision = None`** - Making it the root of the migration tree
2. **Creates the original tables** - Defines `supplier`, `catalog`, and `user` with their original schemas
3. **Enables subsequent migrations** - All other migrations can now run in order

## Migration Chain

The complete migration order is:

```
1c9028d7e8d1_baseline_schema
  └─ Creates original tables: supplier, catalog, user
     └─ down_revision = None

c179efb24a95_alterado_tipo_da_coluna_numero_tel_em_
  └─ Alters supplier.numero_tel from INTEGER to VARCHAR(20)
     └─ down_revision = '1c9028d7e8d1'

0a06e829d578_tb_catalog_exec_change_table_name_and_
  └─ Migrates catalog → tb_catalog (renames id → perfume_id)
     └─ down_revision = 'c179efb24a95'

4060addae700_tb_usuario_exec_changes
  └─ Migrates user → tb_usuario (various column changes)
     └─ down_revision = '0a06e829d578'

8e6249e37efa_tb_fornecedor_changes
  └─ Migrates supplier → tb_fornecedor (various column changes)
     └─ down_revision = '4060addae700'

44855e7e816a_tb_fornecedor_changes_razao_social
  └─ Renames razao → razao_social in tb_fornecedor
     └─ down_revision = '8e6249e37efa'
```

## Baseline Table Schemas

The baseline creates these original tables:

### `supplier` table
```python
- id (Integer, PK)
- razao (String 128, NOT NULL)
- email (String 128)
- cnpj (String 14)
- numero_tel (Integer)  # Originally INTEGER, later changed to VARCHAR
- cep (String 8)
- rua (String 128)
- numero (Integer)
- cidade (String 128)
- uf (String 2)
- pais (String 64)
```

### `catalog` table
```python
- id (Integer, PK)
- perfume (String 128, NOT NULL)
- ml (Integer, NOT NULL)
- tipo (String 128, NOT NULL)
- preco (Float, NOT NULL)
- tags (String 255, NOT NULL)
- imagem_url (String 256)
```

### `user` table
```python
- id (Integer, PK)
- password (String 128, NOT NULL)
- email (String 128, NOT NULL, UNIQUE)
- user (ENUM 'customer'/'admin', NOT NULL)
- nome (String 128, NOT NULL)
- sexo (ENUM 'M'/'F')
- cpf (String 11, NOT NULL, UNIQUE)
- numero_tel (Integer)  # Originally INTEGER
- cep (Integer)  # Originally INTEGER
- rua (String 128)
- numero (Integer)
- cidade (String 128)
- uf (String 2)
```

## Local Development Safety

### Will this affect my existing database?

**No.** The baseline migration is safe for existing databases because:

- Alembic tracks applied migrations in the `alembic_version` table
- It only runs migrations that haven't been applied yet
- If your tables already exist, the baseline is skipped

### Stamping the baseline

For existing local databases that already have the tables, mark the baseline as applied without running it:

```bash
# Mark only the baseline as applied
alembic stamp 1c9028d7e8d1

# Or mark all migrations up to current state as applied
alembic stamp head
```

This tells Alembic "these migrations are already applied" without executing them.

## Verifying Migration State

### Check current migration version

```bash
alembic current
```

Expected output:
```
44855e7e816a (head)
```

### View full migration history

```bash
alembic history --verbose
```

This shows the complete chain with revision IDs and descriptions.

### Test migrations in a fresh database

To verify the migration chain works from scratch (like in CI):

```bash
# Reset database
docker compose down -v
docker compose up -d db

# Run all migrations from baseline
alembic upgrade head
```

## CI/CD Integration

### In GitHub Actions

The baseline migration automatically runs in CI because:

1. CI starts with an empty PostgreSQL database
2. `alembic upgrade head` runs during the test setup
3. The baseline is the first migration, creating all necessary tables
4. Subsequent migrations run in order, transforming the schema

### Workflow example

```yaml
- name: Run migrations
  run: |
    pipenv run alembic upgrade head
  
- name: Run tests
  run: |
    pipenv run pytest
```

## When to Update the Baseline

Update the baseline migration if:

1. ✅ Adding new tables needed before existing migrations
2. ✅ CI tests fail due to missing tables in early migrations
3. ✅ Setting up the project in a new environment for the first time

**Never modify the baseline after:**

1. ❌ It's been deployed to production
2. ❌ It's been merged to the main branch
3. ❌ Other developers have applied it

Instead, create new migrations for schema changes.

## Troubleshooting

### "Table already exists" error

If you get this error locally:

```bash
# Mark the baseline as already applied
alembic stamp 1c9028d7e8d1
```

### "Table doesn't exist" error in CI

Ensure:
1. The baseline `down_revision = None`
2. The next migration has `down_revision = '1c9028d7e8d1'`
3. The baseline creates all tables referenced by subsequent migrations

### Migration order confusion

Run this to see the dependency tree:

```bash
alembic history --verbose
```

Look for the `down_revision` chain to verify correct ordering.

## Best Practices

1. **Keep the baseline minimal** - Only create tables that existed before migration tracking
2. **Use exact schema** - Match original table definitions precisely
3. **Document changes** - Explain why each migration exists
4. **Test in fresh DB** - Verify the chain works from scratch before CI
5. **Don't modify history** - Never change migrations after they're shared/deployed

## Related Documentation

- [DEV_DATABASE.md](DEV_DATABASE.md) - Database setup and Docker Compose
- [Alembic Documentation](https://alembic.sqlalchemy.org/) - Official migration guide
- Migration files: `alembic/versions/`
