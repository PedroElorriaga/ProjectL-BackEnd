"""baseline schema

Revision ID: 1c9028d7e8d1
Revises: None
Create Date: 2026-03-02 22:13:27.096929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1c9028d7e8d1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - creates original tables for CI testing."""
    # Create ENUM types
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE user_types AS ENUM ('customer', 'admin');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE sexo_types AS ENUM ('M', 'F');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create original 'supplier' table (before migrations altered it)
    op.create_table('supplier',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('razao', sa.String(length=128), nullable=False),
                    sa.Column('email', sa.String(length=128), nullable=True),
                    sa.Column('cnpj', sa.String(length=14), nullable=True),
                    sa.Column('numero_tel', sa.Integer(),
                              nullable=True),  # Originally INTEGER
                    sa.Column('cep', sa.String(length=8), nullable=True),
                    sa.Column('rua', sa.String(length=128), nullable=True),
                    sa.Column('numero', sa.Integer(), nullable=True),
                    sa.Column('cidade', sa.String(length=128), nullable=True),
                    sa.Column('uf', sa.String(length=2), nullable=True),
                    sa.Column('pais', sa.String(length=64), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    # Create original 'catalog' table (before migrations altered it)
    op.create_table('catalog',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('perfume', sa.String(
                        length=128), nullable=False),
                    sa.Column('ml', sa.Integer(), nullable=False),
                    sa.Column('tipo', sa.String(length=128), nullable=False),
                    sa.Column('preco', sa.Float(), nullable=False),
                    sa.Column('tags', sa.String(length=255), nullable=False),
                    sa.Column('imagem_url', sa.String(
                        length=256), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )

    # Create original 'user' table (before migrations altered it)
    op.create_table('user',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('password', sa.String(
                        length=128), nullable=False),
                    sa.Column('email', sa.String(length=128), nullable=False),
                    sa.Column('user', postgresql.ENUM('customer', 'admin',
                                                      name='user_types', create_type=False), nullable=False),
                    sa.Column('nome', sa.String(length=128), nullable=False),
                    sa.Column('sexo', postgresql.ENUM(
                        'M', 'F', name='sexo_types', create_type=False), nullable=True),
                    sa.Column('cpf', sa.String(length=11), nullable=False),
                    sa.Column('numero_tel', sa.Integer(),
                              nullable=True),  # Originally INTEGER
                    # Originally INTEGER
                    sa.Column('cep', sa.Integer(), nullable=True),
                    sa.Column('rua', sa.String(length=128), nullable=True),
                    sa.Column('numero', sa.Integer(), nullable=True),
                    sa.Column('cidade', sa.String(length=128), nullable=True),
                    sa.Column('uf', sa.String(length=2), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('cpf'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    """Downgrade schema - drops all baseline tables."""
    op.drop_table('user')
    op.drop_table('catalog')
    op.drop_table('supplier')
    op.execute("DROP TYPE IF EXISTS sexo_types")
    op.execute("DROP TYPE IF EXISTS user_types")
