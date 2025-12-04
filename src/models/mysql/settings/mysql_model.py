from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

# TODO SEPARAR MODELS POR ARQUIVO


class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    perfume = db.Column(
        db.String(128), nullable=False)
    ml = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(128), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tags_string = db.Column('tags', db.String(255), nullable=False)
    imagem_url = db.Column(db.String(256))

    @property
    def tags(self):
        """Retorna as tags como uma lista (array) ao acessar o atributo."""
        if self.tags_string:
            return self.tags_string.split(',')
        return []

    @tags.setter
    def tags(self, tag_list):
        """Salva a lista (array) como uma string delimitada por vírgula."""
        self.tags_string = ','.join(tag_list)


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    user = db.Column(Enum('customer', 'admin', name='user_types'),
                     nullable=False, default='customer')
    nome = db.Column(db.String(128), nullable=False)
    sexo = db.Column(Enum('M', 'F'))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    numero_tel = db.Column(db.Integer)
    cep = db.Column(db.Integer)
    rua = db.Column(db.String(128))
    numero = db.Column(db.Integer)
    cidade = db.Column(db.String(128))
    uf = db.Column(db.String(2))
