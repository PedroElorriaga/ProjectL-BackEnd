from flask_sqlalchemy import SQLAlchemy
from src.models.mysql.settings.mysql_model import Catalog
from typing import List


class CatalogRepository:
    def __init__(self, mysql_connection: SQLAlchemy, table_model: object):
        self.__mysql_connection = mysql_connection
        self.__table_model = table_model

    def add_item(self, data: dict) -> None:
        item_exists = self.search_filtered_item(data)

        if item_exists:
            raise Exception('O item ja existe!')

        new_item = Catalog(
            perfume=data['perfume'],
            ml=data['ml'],
            preco=data['preco'],
            tipo=data['tipo'].upper(),
            tags=data['tags']
        )
        self.__mysql_connection.session.add(new_item)
        self.__mysql_connection.session.commit()

    def get_all_itens(self) -> List[object]:
        itens = self.__table_model.query.all()
        response = []

        if len(itens) == 0:
            raise Exception('Não existe itens no catalogo')

        for item in itens:
            response.append({
                'perfume': item.perfume,
                'ml': item.ml,
                'preco': item.preco,
                'tipo': item.tipo,
                'tags': item.tags,
            })

        return response

    def delete_item(self, id: int) -> None:
        item = self.__table_model.query.get(id)

        if not item:
            raise Exception('Id não existe')

        self.__mysql_connection.session.delete(item)
        self.__mysql_connection.session.commit()

    def patch_item(self, id: int, data: dict) -> None:
        item = self.__table_model.query.get(id)

        if not item:
            raise Exception('Id não existe')

        for field in ['perfume', 'ml', 'preco', 'tipo' 'tags']:
            if field in data:
                setattr(item, field, data[field])

        self.__mysql_connection.session.commit()

    def search_filtered_item(self, data: dict) -> Catalog | None:
        item = (
            self.__mysql_connection.session.query(Catalog)
            .filter(Catalog.perfume == data['perfume'])
            .filter(Catalog.ml == data['ml'])
            .filter(Catalog.tipo == data['tipo'])
            .first()
        )

        return item
