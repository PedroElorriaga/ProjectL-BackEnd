from src.databases.postgres.settings.postgres_config import PostgresDbAlchemy

db = PostgresDbAlchemy.db


class Supplier(db.Model):
    __tablename__ = 'tb_fornecedor'

    fornecedor_id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    cnpj = db.Column(db.String(14))
    numero_tel = db.Column(db.String(20))
    cep = db.Column(db.String(8))
    rua = db.Column(db.String(128))
    numero_endereco = db.Column(db.Integer)
    cidade = db.Column(db.String(128))
    uf = db.Column(db.String(2))
    pais = db.Column(db.String(64))
