from src.databases.postgres.repository.catalog_repository import CatalogRepository
from src.services.http_types.http_response import HttpResponse
from src.main.dtos.catalog_dto import CatalogNewPerfumeRequestDTO, CatalogResponseDTO, CatalogUpdatePerfumeRequestDTO
from sqlalchemy.exc import DataError


class CatalogController:
    def __init__(self, catalog_repository: CatalogRepository):
        self.__catalog_repository = catalog_repository

    def add_new_perfume(self, data: dict, user_token_information: tuple) -> HttpResponse:
        (id, role) = user_token_information

        input_data = CatalogNewPerfumeRequestDTO(**data)

        if role != 'admin':
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Você não tem permissão para executar isso'), 401)

        try:
            self.__catalog_repository.add_item(input_data.model_dump())
            return HttpResponse(CatalogResponseDTO(
                sucess=True, message='Perfume incluido na base de dados!'), 201)
        except KeyError as exc:
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message=F'Falta informações na sua inclusão -> {str(exc)} <-'), 401)
        except DataError as exc:
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Os tipos das informações não estão corretos'), 401)
        except Exception as exc:
            if str(exc) == 'Ocorreu um erro interno ao processar o token':
                return HttpResponse(CatalogResponseDTO(
                    sucess=False, message=str(exc)), 500)
            if str(exc) == 'O item ja existe!':
                return HttpResponse(CatalogResponseDTO(
                    sucess=False, message=str(exc)), 401)
            print(exc)
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Ops :( Algum erro inesperedo ocorreu'), 500)

    def get_perfume(self, id: int | None = None) -> HttpResponse:
        try:
            if id:
                itens = self.__catalog_repository.get_item(id)
            else:
                itens = self.__catalog_repository.get_all_itens()

            if len(itens) == 0:
                return HttpResponse(CatalogResponseDTO(
                    sucess=True, message=itens), 200)

            return HttpResponse(CatalogResponseDTO(
                sucess=True, message=itens), 200)
        except Exception as exc:
            if str(exc) == 'O item não existe no catalogo':
                return HttpResponse(CatalogResponseDTO(
                    sucess=False, message=f'Ops -> {str(exc)} <-'), 404)
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Ops :( Algum erro inesperedo ocorreu'), 500)

    def delete_perfume(self, id_perfume: int, user_token_information: tuple) -> HttpResponse:
        (id, role) = user_token_information

        if role != 'admin':
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Você não tem permissão para executar isso'), 401)

        try:
            self.__catalog_repository.delete_item(id_perfume)

            return HttpResponse(CatalogResponseDTO(
                                sucess=True, message='Item deletado com sucesso!'), 200)
        except Exception as exc:
            if str(exc) == 'Id não existe':
                return HttpResponse(CatalogResponseDTO(
                    sucess=False, message=f'Ops -> {str(exc)} <-'), 404)
            print(exc)
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Ops :( Algum erro inesperedo ocorreu'), 500)

    def patch_perfume(self, id_perfume: int, data: dict, user_token_information: tuple) -> HttpResponse:
        (id, role) = user_token_information

        input_data = CatalogUpdatePerfumeRequestDTO(**data)

        if role != 'admin':
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Você não tem permissão para executar isso'), 401)

        try:
            self.__catalog_repository.patch_item(id_perfume, input_data)

            return HttpResponse(CatalogResponseDTO(
                sucess=True, message='Item atualizado com sucesso!'), 200)
        except Exception as exc:
            if str(exc) == 'Id não existe':
                return HttpResponse(CatalogResponseDTO(
                    sucess=False, message=f'Ops -> {str(exc)} <-'), 404)
            print(exc)
            return HttpResponse(CatalogResponseDTO(
                sucess=False, message='Ops :( Algum erro inesperedo ocorreu'), 500)

    def get_filtered_perfumes(self, data: dict) -> HttpResponse:
        itens = self.__catalog_repository.get_all_itens_filtered(data)

        return HttpResponse(CatalogResponseDTO(
            sucess=True, message=itens), 200)
