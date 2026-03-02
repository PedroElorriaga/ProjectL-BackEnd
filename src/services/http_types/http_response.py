from src.modules.login.dtos.login_dto import LoginResponseDTO
from src.modules.catalog.dtos.catalog_dto import CatalogResponseDTO
from src.main.dtos.supplier_dto import SupplierResponseDTO


class HttpResponse:
    def __init__(self, body: LoginResponseDTO | CatalogResponseDTO | SupplierResponseDTO, status: int):
        self.body = body
        self.status = status
