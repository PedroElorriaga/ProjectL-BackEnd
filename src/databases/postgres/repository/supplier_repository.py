from flask_sqlalchemy import SQLAlchemy
from typing import List


class SupplierRepository:
    def __init__(self, mysql_connection: SQLAlchemy, table_model: object):
        self.__mysql_connection = mysql_connection
        self.__table_model = table_model

    def get_all_itens(self) -> List[dict] | List[None]:
        itens = self.__table_model.query.all()
        list_itens = []

        for item in itens:
            list_itens.append({
                'id': item.id,
                'razao': item.razao,
                'email': item.email,
                'cnpj': item.cnpj,
                'numero_tel': item.numero_tel,
                'cep': item.cep,
                'rua': item.rua,
                'numero': item.numero,
                'cidade': item.cidade,
                'uf': item.uf,
                'pais': item.pais
            })

        return list_itens

    def get_item_by_id(self, id_item: int) -> dict | None:
        item = self.__table_model.query.get(id_item)

        dict_item = {
            'id': item.id,
            'razao': item.razao,
            'email': item.email,
            'cnpj': item.cnpj,
            'numero_tel': item.numero_tel,
            'cep': item.cep,
            'rua': item.rua,
            'numero': item.numero,
            'cidade': item.cidade,
            'uf': item.uf,
            'pais': item.pais
        }

        return dict_item
