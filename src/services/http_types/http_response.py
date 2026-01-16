from src.main.dtos.login_dto import LoginResponseDTO
from src.main.dtos.catalog_dto import CatalogResponseDTO


class HttpResponse:
    def __init__(self, body: LoginResponseDTO | CatalogResponseDTO, status: int):
        self.body = body
        self.status = status
