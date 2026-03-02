from src.modules.users.repositories.user_repository import UserRepository
from src.services.http_types.http_response import HttpResponse
from sqlalchemy.exc import IntegrityError
from src.services.security.bcrypt.bcrypt_handle import BcryptHandle
from src.services.security.jwt.jwt_handle import JwtHandle
from src.modules.users.dtos.user_dto import UserResponseDTO, UserCreateRequestDTO
from validate_docbr import CPF


class UserController:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def create_user(self, data: dict) -> HttpResponse:
        try:
            user_input_data = UserCreateRequestDTO(**data)
            # TODO - VALIDAR SE TEM CARACTERES ESPECIAIS
            cpf = CPF()

            # TODO - COLOCAR EM UM SERVICE DE VALIDATION
            if not cpf.validate(user_input_data.cpf):
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='Cpf inválido'), 401)

            password_hashed = BcryptHandle.hash_content(
                user_input_data.senha)
            user_input_data.senha = password_hashed

            self.__user_repository.create_new_item(
                user_input_data.model_dump())

            return HttpResponse(UserResponseDTO(
                sucess=True, message='Usuário criado com sucesso'), 201)
        except IntegrityError as exc:
            if user_input_data.get('email') in str(exc).split('")')[0]:
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='O email já esta sendo utilizado'), 401)
            elif user_input_data.get('cpf') in str(exc).split('")')[0]:
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='O cpf já esta sendo utilizado'), 401)
        except Exception as exc:
            if 'validation error for NewLoginRequestDTO' in str(exc):
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='Email inválido'), 400)
            print(exc)
            return HttpResponse(UserResponseDTO(
                sucess=False, message='Ocorreu algum erro inesperado'), 500)
