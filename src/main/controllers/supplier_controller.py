from src.databases.postgres.repository.supplier_repository import SupplierRepository
from src.services.http_types.http_response import HttpResponse
from src.main.dtos.supplier_dto import SupplierResponseDTO, SupplierCreateRequestDTO, SupplierUpdateRequestDTO


class SuplierController:
    def __init__(self, supplier_repository: SupplierRepository):
        self.__supplier_repository = supplier_repository

    def get_supplier(self, user_token_information: tuple, id_supplier: int = None) -> HttpResponse:
        try:
            if not self.__check_if_is_admin(user_token_information):
                return HttpResponse(SupplierResponseDTO(
                    sucess=False, message='Você não tem permissão para executar isso'), 401)

            if id_supplier:
                itens = self.__supplier_repository.get_item_by_id(id_supplier)
            else:
                itens = self.__supplier_repository.get_all_itens()

            if not itens:
                return HttpResponse(SupplierResponseDTO(
                    sucess=True, message='O(s) fornecedor(s) não existe(m)'
                ), 204)

            return HttpResponse(SupplierResponseDTO(
                sucess=True, message=itens
            ), 200)
        except Exception as exc:
            print(exc)
            return HttpResponse(SupplierResponseDTO(
                sucess=False, message='Ocorreu algum erro inesperado'), 500)

    def create_supplier(self, user_token_information: tuple, supplier_datas: dict) -> HttpResponse:
        try:
            if not self.__check_if_is_admin(user_token_information):
                return HttpResponse(SupplierResponseDTO(
                    sucess=False, message='Você não tem permissão para executar isso'), 401)

            user_input_data = SupplierCreateRequestDTO(**supplier_datas)
            self.__supplier_repository.create_new_item(user_input_data)

            return HttpResponse(SupplierResponseDTO(
                sucess=True, message='Fornecedor incluido com sucesso'), 201)
        except Exception as exc:
            print(exc)
            return HttpResponse(SupplierResponseDTO(
                sucess=False, message='Ocorreu algum erro inesperado'), 500)

    def update_supplier(self, user_token_information: tuple, id_supplier: int, supplier_datas: dict) -> HttpResponse:
        try:
            if not self.__check_if_is_admin(user_token_information):
                return HttpResponse(SupplierResponseDTO(
                    sucess=False, message='Você não tem permissão para executar isso'), 401)

            user_input_data = SupplierUpdateRequestDTO(**supplier_datas)

            self.__supplier_repository.update_item_by_id(
                id_supplier, user_input_data)

            return HttpResponse(SupplierResponseDTO(
                sucess=True, message='Fornecedor atualizado com sucesso'), 200)
        except FileNotFoundError:
            return HttpResponse(SupplierResponseDTO(
                sucess=False, message='Fornecedor não encontrado'), 404)
        except Exception as exc:
            print(exc)
            return HttpResponse(SupplierResponseDTO(
                sucess=False, message='Ocorreu algum erro inesperado'), 500)

    def delete_supplier(self, user_token_information: tuple, id_supplier: int) -> HttpResponse:
        try:
            if not self.__check_if_is_admin(user_token_information):
                return HttpResponse(SupplierResponseDTO(
                    sucess=False, message='Você não tem permissão para executar isso'), 401)

            self.__supplier_repository.delete_item_by_id(id_supplier)

            return HttpResponse(SupplierResponseDTO(
                sucess=True, message='Fornecedor deletado com sucesso'), 200)
        except FileNotFoundError:
            return HttpResponse(SupplierResponseDTO(
                sucess=False, message='Fornecedor não encontrado'), 404)
        except Exception as exc:
            print(exc)

    def __check_if_is_admin(self, user_token_information: tuple) -> bool:
        (id, role) = user_token_information

        if role != 'admin':
            return False

        return True
