from src.databases.postgres.settings.postgres_config import PostgresDbAlchemy

db = PostgresDbAlchemy.db


class Catalog(db.Model):
    __tablename__ = 'catalog'

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
