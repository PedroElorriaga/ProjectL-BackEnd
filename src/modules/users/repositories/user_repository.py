from flask_sqlalchemy import SQLAlchemy
from src.modules.users.models.user import User


class UserRepository:
    def __init__(self, mysql_connection: SQLAlchemy, table_model: object):
        self.__mysql_connection = mysql_connection
        self.__table_model = table_model

    def create_new_item(self, data: dict) -> None:
        item = User(
            hash_senha=data['senha'],
            email=data['email'],
            tipo_usuario='customer',
            nome=data['nome'],
            sexo=data.get('sexo'),
            cpf=data['cpf'],
            numero_tel=data.get('numero_tel'),
            cep=data.get('cep'),
            rua=data.get('rua'),
            numero_residencia=data.get('numero_residencia'),
            cidade=data.get('cidade'),
            uf=data.get('uf'),
        )
        self.__mysql_connection.session.add(item)
        self.__mysql_connection.session.commit()

    def get_item(self, email: str, id: int | None = None) -> User:
        if id:
            item = self.__table_model.query.get(id)
            if not item:
                raise Exception('Nenhum item foi encontrado com esse ID')

            return item

        item = self.__table_model.query.filter_by(email=email).first()
        if not item:
            raise Exception('Nenhum item foi encontrado com esse EMAIL')

        return item
