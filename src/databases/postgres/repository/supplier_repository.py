from flask_sqlalchemy import SQLAlchemy
from typing import List
from src.main.dtos.supplier_dto import SupplierCreateRequestDTO
from src.databases.postgres.model.supplier import Supplier


class SupplierRepository:
    def __init__(self, mysql_connection: SQLAlchemy, table_model: object):
        self.__mysql_connection = mysql_connection  # ACAO DENTRO DO DB
        self.__table_model = table_model  # QUERY DENTRO DO DB

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

        if not item:
            return None

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

    def create_new_item(self, item_datas: SupplierCreateRequestDTO) -> None:
        item = Supplier(
            razao=item_datas.razao,
            email=item_datas.email,
            cnpj=item_datas.cnpj,
            numero_tel=item_datas.numero_tel,
            cep=item_datas.cep,
            rua=item_datas.rua,
            numero=item_datas.numero,
            cidade=item_datas.cidade,
            uf=item_datas.uf,
            pais=item_datas.pais
        )

        self.__mysql_connection.session.add(item)
        self.__mysql_connection.session.commit()

    def update_item_by_id(self, id_item: int, item_datas: SupplierCreateRequestDTO) -> None:
        item = self.__table_model.query.get(id_item)

        if not item:
            raise FileNotFoundError('Item não foi encontrado')

        data_dump = item_datas.model_dump()

        for field in ['razao', 'email', 'cnpj', 'numero_tel', 'cep', 'rua', 'numero', 'cidade', 'uf', 'pais']:
            if field in data_dump:
                if data_dump[field]:
                    setattr(item, field, data_dump[field])

        self.__mysql_connection.session.commit()

    def delete_item_by_id(self, id_item: int) -> None:
        item = self.__table_model.query.get(id_item)

        if not item:
            raise FileNotFoundError('Item não foi encontrado')

        self.__mysql_connection.session.delete(item)
        self.__mysql_connection.session.commit()
