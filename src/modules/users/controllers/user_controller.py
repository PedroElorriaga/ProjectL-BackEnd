from src.modules.users.repositories.user_repository import UserRepository
from src.shared.http_types.http_response import HttpResponse
from sqlalchemy.exc import IntegrityError
from src.services.security.bcrypt.bcrypt_handle import BcryptHandle
from src.modules.users.dtos.user_dto import UserResponseDTO, UserCreateRequestDTO
from src.services.security.password.password_validator import PasswordValidator
from src.services.cpf_service.cpf_validator import CPFValidator


class UserController:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def create_user(self, data: dict) -> HttpResponse:
        try:
            user_input_data = UserCreateRequestDTO(**data)
            password_validator = PasswordValidator.validate(
                user_input_data.senha)
            is_valid_cpf, cleaned_cpf = CPFValidator.validate(
                user_input_data.cpf)

            if not password_validator:
                return HttpResponse(UserResponseDTO(
                    sucess=False,
                    message='A senha deve conter no mínimo 8 caracteres, '
                    'incluindo letras maiúsculas, minúsculas, números e caracteres especiais'), 400)

            if not is_valid_cpf:
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='Cpf inválido'), 401)

            user_input_data.cpf = cleaned_cpf

            password_hashed = BcryptHandle.hash_content(
                user_input_data.senha)
            user_input_data.senha = password_hashed

            self.__user_repository.create_new_item(
                user_input_data.model_dump())

            return HttpResponse(UserResponseDTO(
                sucess=True, message='Usuário criado com sucesso'), 201)
        except IntegrityError as exc:
            if f'DETAIL:  Key (cpf)=({user_input_data.cpf}) already exists.' in str(exc):
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='O cpf já esta sendo utilizado'), 401)
            elif f'DETAIL:  Key (email)=({user_input_data.email}) already exists.' in str(exc):
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='O email já esta sendo utilizado'), 401)
        except Exception as exc:
            print(exc)
            if 'validation error for UserCreateRequestDTO' in str(exc):
                return HttpResponse(UserResponseDTO(
                    sucess=False, message='Email inválido'), 400)
            return HttpResponse(UserResponseDTO(
                sucess=False, message='Ocorreu algum erro inesperado'), 500)
