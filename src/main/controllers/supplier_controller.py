from src.databases.postgres.repository.supplier_repository import SupplierRepository
from src.services.http_types.http_response import HttpResponse
from src.main.dtos.supplier_dto import SupplierResponseDTO


class SuplierController:
    def __init__(self, supplier_repository: SupplierRepository):
        self.__supplier_repository = supplier_repository

    def get_all_suppliers(self) -> HttpResponse:
        itens = self.__supplier_repository.get_all_itens()

        return HttpResponse(SupplierResponseDTO(
            sucess=True, message=itens
        ), 200)
