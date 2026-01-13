from flask_sqlalchemy import SQLAlchemy
from src.databases.postgres.model.catalog import Catalog
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
            perfume=data['perfume'].lower(),
            ml=data['ml'],
            preco=data['preco'],
            tipo=data['tipo'].upper(),
            tags=data['tags'],
            imagem_url=data['imagem_url']
        )
        self.__mysql_connection.session.add(new_item)
        self.__mysql_connection.session.commit()

    def get_all_itens(self) -> List[object] | List[None]:
        itens = self.__table_model.query.all()
        response = []

        if len(itens) == 0:
            return response

        for item in itens:
            response.append({
                'id': item.id,
                'perfume': item.perfume,
                'ml': item.ml,
                'preco': item.preco,
                'tipo': item.tipo,
                'tags': item.tags,
                'imagem_url': item.imagem_url
            })

        return response

    def get_item(self, id: int) -> dict | None:
        item = self.__table_model.query.get(id)

        if not item:
            raise Exception('O item não existe no catalogo')

        response = {
            'id': item.id,
            'perfume': item.perfume,
            'ml': item.ml,
            'preco': item.preco,
            'tipo': item.tipo,
            'tags': item.tags,
            'imagem_url': item.imagem_url
        }

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

        for field in ['perfume', 'ml', 'preco', 'tipo', 'tags', 'imagem_url']:
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

    def get_all_itens_filtered(self, data: dict) -> List[object] | None:
        for field in ['perfume', 'ml', 'preco', 'tipo', 'tags_string']:
            if field in data and data[field]:
                # getattr transforma a string 'perfume' em Catalog.perfume - NAO ESQUECE PEDRONAUTA
                column = getattr(Catalog, field)
                itens = self.__mysql_connection.session.query(Catalog).filter(
                    column.contains(data[field])).all()
                break

        response = []
        for item in itens:
            response.append({
                'id': item.id,
                'perfume': item.perfume,
                'ml': item.ml,
                'preco': item.preco,
                'tipo': item.tipo,
                'tags': item.tags,
                'imagem_url': item.imagem_url
            })

        return response
