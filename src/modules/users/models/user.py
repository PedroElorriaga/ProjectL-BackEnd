from src.databases.postgres.settings.postgres_config import PostgresDbAlchemy
from sqlalchemy import Enum

db = PostgresDbAlchemy.db


class User(db.Model):
    __tablename__ = 'tb_usuario'

    id = db.Column(db.Integer, primary_key=True)
    hash_senha = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    tipo_usuario = db.Column(Enum('customer', 'admin', name='user_types'),
                             nullable=False, default='customer')
    nome = db.Column(db.String(128), nullable=False)
    sexo = db.Column(Enum('M', 'F', name='sexo_types'))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    numero_tel = db.Column(db.String(15))
    cep = db.Column(db.String(10))
    rua = db.Column(db.String(128))
    numero_residencia = db.Column(db.Integer)
    cidade = db.Column(db.String(128))
    uf = db.Column(db.String(2))
