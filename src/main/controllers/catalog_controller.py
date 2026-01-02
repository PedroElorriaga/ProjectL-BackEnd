from src.models.mysql.repository.catalog_repository import CatalogRepository
from src.services.http_types.http_response import HttpResponse
from sqlalchemy.exc import DataError


class CatalogController:
    def __init__(self, catalog_repository: CatalogRepository):
        self.__catalog_repository = catalog_repository

    def add_new_perfume(self, data: dict, user_token_information: tuple) -> HttpResponse:
        (id, role) = user_token_information

        if role != 'admin':
            return HttpResponse({'sucess': False, 'message': f'Você não tem permissão para executar isso'}, 401)

        try:
            self.__catalog_repository.add_item(data)
            return HttpResponse({'sucess': True, 'message': 'Perfume incluido na base de dados!'}, 200)
        except KeyError as exc:
            return HttpResponse({'sucess': False, 'message': f'Falta informações na sua inclusão -> {str(exc)} <-'}, 401)
        except DataError as exc:
            return HttpResponse({'sucess': False, 'message': f'Os tipos das informações não estão corretos'}, 401)
        except Exception as exc:
            if str(exc) == 'Ocorreu um erro interno ao processar o token':
                return HttpResponse({'sucess': False, 'message': str(exc)}, 500)
            if str(exc) == 'O item ja existe!':
                return HttpResponse({'sucess': False, 'message': str(exc)}, 401)
            print(exc)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)

    def get_perfume(self, id: int | None = None) -> HttpResponse:
        try:
            if id:
                response = self.__catalog_repository.get_item(id)
            else:
                response = self.__catalog_repository.get_all_itens()

            return HttpResponse({'sucess': True, 'message': response}, 200)
        except Exception as exc:
            if str(exc) == 'Não esse item no catalogo':
                return HttpResponse({'sucess': False, 'message': f'Ops -> {str(exc)} <-'}, 404)
            if str(exc) == 'Não existe itens no catalogo':
                return HttpResponse({'sucess': False, 'message': f'Ops -> {str(exc)} <-'}, 404)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)

    def delete_perfume(self, id_perfume: int, user_token_information: tuple) -> HttpResponse:
        (id, role) = user_token_information

        if role != 'admin':
            return HttpResponse({'sucess': False, 'message': f'Você não tem permissão para executar isso'}, 401)

        try:
            self.__catalog_repository.delete_item(id_perfume)

            return HttpResponse({'sucess': True, 'message': 'Item deletado com sucesso!'}, 200)
        except Exception as exc:
            if str(exc) == 'Id não existe':
                return HttpResponse({'sucess': False, 'message': f'Ops -> {str(exc)} <-'}, 404)
            print(exc)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)

    def patch_perfume(self, id_perfume: int, data: dict, user_token_information: tuple) -> HttpResponse:
        (id, role) = user_token_information

        if role != 'admin':
            return HttpResponse({'sucess': False, 'message': f'Você não tem permissão para executar isso'}, 401)

        try:
            self.__catalog_repository.patch_item(id_perfume, data)

            return HttpResponse({'sucess': True, 'message': 'Item atualizado com sucesso!'}, 200)
        except Exception as exc:
            if str(exc) == 'Id não existe':
                return HttpResponse({'sucess': False, 'message': f'Ops -> {str(exc)} <-'}, 404)
            print(exc)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)
