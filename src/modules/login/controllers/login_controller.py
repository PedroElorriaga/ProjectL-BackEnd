from src.modules.users.repositories.user_repository import UserRepository
from src.shared.http_types.http_response import HttpResponse
from src.services.security.bcrypt.bcrypt_handle import BcryptHandle
from src.services.security.jwt.jwt_handle import JwtHandle
from src.modules.login.dtos.login_dto import LoginResponseDTO, LoginRequestDTO


class LoginController:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def get_login_credentials(self, data: dict, id: int | None = None) -> HttpResponse:
        try:
            input_data = LoginRequestDTO(**data)

            user_credential = self.__user_repository.get_item(
                input_data.email, id)

            if not BcryptHandle.check_content(input_data.senha, user_credential.hash_senha):
                return HttpResponse(LoginResponseDTO(
                    sucess=False, message='Credenciais inválidas. Verifique seu email e senha.'), 401)

            access_token = JwtHandle.gen_token(
                user_credential.id, user_credential.tipo_usuario)

            return HttpResponse(LoginResponseDTO(
                sucess=True, message='Login Efetuado com sucesso', access_token=access_token), 200)
        except Exception as exc:
            if str(exc) == 'Nenhum item foi encontrado com esse ID':
                return HttpResponse(LoginResponseDTO(
                    sucess=False, message='Parece que esse ID não existe'), 404)
            elif str(exc) == 'Nenhum item foi encontrado com esse EMAIL':
                return HttpResponse(LoginResponseDTO(
                    sucess=False, message='Parece que esse EMAIL não existe'), 404)
            elif 'validation error for LoginRequestDTO' in str(exc):
                return HttpResponse(LoginResponseDTO(
                    sucess=False, message='Email inválido'), 400)
            return HttpResponse(LoginResponseDTO(
                sucess=False, message='Ops :( Algum erro inesperedo ocorreu'), 500)
