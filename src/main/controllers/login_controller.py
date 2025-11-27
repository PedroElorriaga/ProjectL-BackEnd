from src.models.mysql.repository.login_repository import LoginRepository
from src.services.http_types.http_response import HttpResponse
from sqlalchemy.exc import IntegrityError
from src.services.security.bcrypt.bcrypt_handle import BcryptHandle
from src.services.security.jwt.jwt_handle import JwtHandle


class LoginController:
    def __init__(self, login_repository: LoginRepository):
        self.__login_repository = login_repository

    def add_new_login(self, data: dict) -> HttpResponse:
        try:
            password_hashed = BcryptHandle.hash_content(data['password'])
            data['password'] = password_hashed

            self.__login_repository.add_item(data)

            return HttpResponse({'sucess': True, 'message': 'Login criado com sucesso!'}, 200)
        except IntegrityError as exc:
            if data.get('email') in str(exc).split('")')[0]:
                return HttpResponse({'sucess': False, 'message': f'O email já esta sendo utilizado'}, 401)
            elif data.get('cpf') in str(exc).split('")')[0]:
                return HttpResponse({'sucess': False, 'message': f'O cpf já esta sendo utilizado'}, 401)
        except Exception as exc:
            print(exc)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)

    def get_login_credentials(self, data: dict, id: int | None = None) -> HttpResponse:
        try:
            login_credential = self.__login_repository.get_item(data, id)

            if not BcryptHandle.check_content(data['password'], login_credential.password):
                return HttpResponse(
                    {'sucess': False, 'message': 'Email ou senha incorretos'}, 401)

            token_response = JwtHandle().gen_token(
                login_credential.id, login_credential.user)

            return HttpResponse({'sucess': True, 'message': 'Login Efetuado com sucesso', 'token': token_response}, 200)
        except Exception as exc:
            if str(exc) == 'Nenhum item foi encontrado com esse ID':
                return HttpResponse({'sucess': False, 'message': 'Parece que esse ID não existe'}, 404)
            elif str(exc) == 'Nenhum item foi encontrado com esse EMAIL':
                return HttpResponse({'sucess': False, 'message': 'Parece que esse EMAIL não existe'}, 404)

            print(exc)
            return HttpResponse({'sucess': False, 'message': f'Ops :( Algum erro inesperedo ocorreu'}, 500)
