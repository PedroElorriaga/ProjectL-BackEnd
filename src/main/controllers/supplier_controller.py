from src.databases.postgres.repository.supplier_repository import SupplierRepository
from src.services.http_types.http_response import HttpResponse
from src.main.dtos.supplier_dto import SupplierResponseDTO


class SuplierController:
    def __init__(self, supplier_repository: SupplierRepository):
        self.__supplier_repository = supplier_repository

    def get_supplier(self, user_token_information: tuple, id_supplier: int = None) -> HttpResponse:
        (id, user_role) = user_token_information

        if user_role != 'admin':
            return HttpResponse(SupplierResponseDTO(
                sucess=False, message='Você não tem permissão para executar isso'), 401)

        try:
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
