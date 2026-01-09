from src.databases.postgres.settings.postgres_config import PostgresDbAlchemy
from sqlalchemy import Enum

db = PostgresDbAlchemy.db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    user = db.Column(Enum('customer', 'admin', name='user_types'),
                     nullable=False, default='customer')
    nome = db.Column(db.String(128), nullable=False)
    sexo = db.Column(Enum('M', 'F', name='sexo_types'))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    numero_tel = db.Column(db.Integer)
    cep = db.Column(db.Integer)
    rua = db.Column(db.String(128))
    numero = db.Column(db.Integer)
    cidade = db.Column(db.String(128))
    uf = db.Column(db.String(2))
