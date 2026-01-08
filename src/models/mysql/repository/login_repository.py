from flask_sqlalchemy import SQLAlchemy
from src.models.mysql.settings.mysql_model import Login


class LoginRepository:
    def __init__(self, mysql_connection: SQLAlchemy, table_model: object):
        self.__mysql_connection = mysql_connection
        self.__table_model = table_model

    def add_item(self, data: dict) -> None:
        new_login = Login(
            password=data['password'],
            email=data['email'],
            user=data['user'],
            nome=data['nome'],
            sexo=data.get('sexo'),
            cpf=data['cpf'],
            numero_tel=data.get('numero_tel'),
            cep=data.get('cep'),
            rua=data.get('rua'),
            numero=data.get('numero'),
            cidade=data.get('cidade'),
            uf=data.get('uf'),
        )
        self.__mysql_connection.session.add(new_login)
        self.__mysql_connection.session.commit()

    def get_item(self, email: str, id: int | None = None) -> Login:
        if id:
            item = self.__table_model.query.get(id)
            if not item:
                raise Exception('Nenhum item foi encontrado com esse ID')

            return item

        item = self.__table_model.query.filter_by(email=email).first()
        if not item:
            raise Exception('Nenhum item foi encontrado com esse EMAIL')

        return item
