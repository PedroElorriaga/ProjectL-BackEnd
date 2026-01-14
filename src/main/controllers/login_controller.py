from src.databases.postgres.repository.user_repository import UserRepository
from src.services.http_types.http_response import HttpResponse
from sqlalchemy.exc import IntegrityError
from src.services.security.bcrypt.bcrypt_handle import BcryptHandle
from src.services.security.jwt.jwt_handle import JwtHandle
from src.main.dtos.login_dto import LoginResponseDTO, LoginRequestDTO, NewLoginRequestDTO
from validate_docbr import CPF


class LoginController:
    def __init__(self, login_repository: UserRepository):
        self.__login_repository = login_repository

    def add_new_login(self, data: dict) -> HttpResponse:
        try:
            input_data = NewLoginRequestDTO(**data)
            # TODO - VALIDAR SE TEM CARACTERES ESPECIAIS
            cpf = CPF()

            if not cpf.validate(input_data.cpf):
                return HttpResponse({'sucess': False, 'message': f'Cpf inválido'}, 401)

            password_hashed = BcryptHandle.hash_content(input_data.password)
            input_data.password = password_hashed

            self.__login_repository.add_item(input_data.model_dump())

            return HttpResponse({'sucess': True, 'message': 'Login criado com sucesso!'}, 201)
        except IntegrityError as exc:
            if data.get('email') in str(exc).split('")')[0]:
                return HttpResponse({'sucess': False, 'message': f'O email já esta sendo utilizado'}, 401)
            elif data.get('cpf') in str(exc).split('")')[0]:
                return HttpResponse({'sucess': False, 'message': f'O cpf já esta sendo utilizado'}, 401)
        except Exception as exc:
            if 'validation error for NewLoginRequestDTO' in str(exc):
                return HttpResponse({'sucess': False, 'message': f'Email inválido'}, 400)
            print(exc)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)

    def get_login_credentials(self, data: dict, id: int | None = None) -> HttpResponse:
        try:
            input_data = LoginRequestDTO(**data)

            login_credential = self.__login_repository.get_item(
                input_data.email, id)

            if not BcryptHandle.check_content(input_data.password, login_credential.password):
                return HttpResponse(
                    {'sucess': False, 'message': 'Email ou senha incorretos'}, 401)

            access_token = JwtHandle.gen_token(
                login_credential.id, login_credential.user)

            return HttpResponse(LoginResponseDTO(
                sucess=True, message='Login Efetuado com sucesso', access_token=access_token), 200)
        except Exception as exc:
            if str(exc) == 'Nenhum item foi encontrado com esse ID':
                return HttpResponse({'sucess': False, 'message': 'Parece que esse ID não existe'}, 404)
            elif str(exc) == 'Nenhum item foi encontrado com esse EMAIL':
                return HttpResponse({'sucess': False, 'message': 'Parece que esse EMAIL não existe'}, 404)

            print(exc)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)
