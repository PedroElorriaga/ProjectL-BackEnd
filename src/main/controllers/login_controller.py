from src.modules.users.repositories.user_repository import UserRepository
from src.services.http_types.http_response import HttpResponse
from src.services.security.bcrypt.bcrypt_handle import BcryptHandle
from src.services.security.jwt.jwt_handle import JwtHandle
from src.main.dtos.login_dto import LoginResponseDTO, LoginRequestDTO


class LoginController:
    def __init__(self, login_repository: UserRepository):
        self.__login_repository = login_repository

    def get_login_credentials(self, data: dict, id: int | None = None) -> HttpResponse:
        try:
            input_data = LoginRequestDTO(**data)

            login_credential = self.__login_repository.get_item(
                input_data.email, id)

            if not BcryptHandle.check_content(input_data.password, login_credential.password):
                return HttpResponse(LoginResponseDTO(
                    sucess=False, message='Email ou senha incorretos'), 401)

            access_token = JwtHandle.gen_token(
                login_credential.id, login_credential.user)

            return HttpResponse(LoginResponseDTO(
                sucess=True, message='Login Efetuado com sucesso', access_token=access_token), 200)
        except Exception as exc:
            if str(exc) == 'Nenhum item foi encontrado com esse ID':
                return HttpResponse(LoginResponseDTO(
                    sucess=False, message='Parece que esse ID não existe'), 404)
            elif str(exc) == 'Nenhum item foi encontrado com esse EMAIL':
                return HttpResponse(LoginResponseDTO(
                    sucess=False, message='Parece que esse EMAIL não existe'), 404)
            print(exc)
            return HttpResponse(LoginResponseDTO(
                sucess=False, message='Ops :( Algum erro inesperedo ocorreu'), 500)
