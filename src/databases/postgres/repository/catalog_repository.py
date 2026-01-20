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

    # TODO - AJUSTAR O TIPO OBJECT PARA dict, ABRIR PR PARA CONTROLE
    def get_all_itens(self) -> List[object] | List[None]:
        itens = self.__table_model.query.all()
        list_itens = []

        for item in itens:
            list_itens.append({
                'id': item.id,
                'perfume': item.perfume,
                'ml': item.ml,
                'preco': item.preco,
                'tipo': item.tipo,
                'tags': item.tags,
                'imagem_url': item.imagem_url
            })

        return list_itens

    # TODO - NOME PODE MELHORAR get_item_by_id SUGESTÃO**, ABRIR PR PARA CONTROLE
    def get_item(self, id: int) -> dict | None:
        item = self.__table_model.query.get(id)

        if not item:
            raise Exception('O item não existe no catalogo')

        dict_item = {
            'id': item.id,
            'perfume': item.perfume,
            'ml': item.ml,
            'preco': item.preco,
            'tipo': item.tipo,
            'tags': item.tags,
            'imagem_url': item.imagem_url
        }

        return dict_item

    def delete_item(self, id: int) -> None:
        item = self.__table_model.query.get(id)

        if not item:
            raise Exception('Id não existe')

        self.__mysql_connection.session.delete(item)
        self.__mysql_connection.session.commit()

    def patch_item(self, id: int, data: dict) -> None:
        item = self.__table_model.query.get(id)
        data_dump = data.model_dump()

        item_exists = self.search_filtered_item(data_dump)
        if item_exists:
            raise Exception('O item ja existe!')

        if not item:
            raise Exception('Id não existe')

        for field in ['perfume', 'ml', 'preco', 'tipo', 'tags', 'imagem_url']:
            if field in data_dump:
                if data_dump[field]:
                    setattr(item, field, data_dump[field])

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

    # TODO - AJUSTAR O TIPO OBJECT PARA dict, ABRIR PR PARA CONTROLE
    def get_all_itens_filtered(self, data: dict) -> List[object] | None:
        for field in ['perfume', 'ml', 'preco', 'tipo', 'tags_string']:
            if field in data and data[field]:
                # getattr transforma a string 'perfume' em Catalog.perfume - NAO ESQUECE PEDRONAUTA
                column = getattr(Catalog, field)
                itens = self.__mysql_connection.session.query(Catalog).filter(
                    column.contains(data[field])).all()
                break

        list_itens = []
        for item in itens:
            list_itens.append({
                'id': item.id,
                'perfume': item.perfume,
                'ml': item.ml,
                'preco': item.preco,
                'tipo': item.tipo,
                'tags': item.tags,
                'imagem_url': item.imagem_url
            })

        return list_itens
