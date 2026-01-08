from src.main.dtos.login_dto import LoginResponseDTO


class HttpResponse:
    def __init__(self, body: LoginResponseDTO, status: int):
        self.body = body
        self.status = status
