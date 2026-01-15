import pytest
import os
import jwt
from app import create_app
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from src.services.http_types.http_response import HttpResponse

load_dotenv()


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_token():
    token = jwt.encode({'public_id': 1, 'user_role': 'admin'},
                       os.getenv('SECRET_KEY'), algorithm='HS256')
    return token


@pytest.fixture
def non_admin_token():
    token = jwt.encode({'public_id': 377, 'user_role': 'customer'},
                       os.getenv('SECRET_KEY'), algorithm='HS256')
    return token


@pytest.fixture
def user():
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.user = 'mock'
    mock_user.email = 'MOCKADO@email.com'
    mock_user.password = 'mock123@'
    return mock_user


@pytest.fixture
def product():
    mock_product = MagicMock()
    mock_product.id = 1
    mock_product.perfume = 'TESTER'
    mock_product.ml = 100
    mock_product.preco = 299.99
    mock_product.tipo = 'EDP'
    mock_product.tags = ['MOCK', 'ADO']
    mock_product.imagem_url = 'url:cloudinary'

    return mock_product


def test_get_root_return_302(client):
    response = client.get('/')

    assert response.status_code == 302


def test_get_catalog_return_200_content_type_json_return_list(client):
    response = client.get('/catalogo/')

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert isinstance(data['message'], list)


def test_get_catalog_return_204_content_type_json_return_list(client):
    with patch('src.databases.postgres.repository.catalog_repository.CatalogRepository.get_all_itens') as mock_repo:
        mock_repo.return_value = []
        response = client.get('/catalogo/')

    assert response.status_code == 204
    assert response.content_type == 'application/json'


def test_post_catalog_add_perfume_with_valid_token_return_201_return_dict(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    payload = {
        'perfume': 'MOCKADO',
        'ml': 999,
        'tipo': 'EDP',
        'preco': '999.99',
        'tags': 'mock_1, mock_2'
    }

    # NAO ESQUECER FUTURAMENTE PEDRONAUTA, AQUI O PATCH NAO DEIXA EXECUTAR O CODIGO ORIGINAL, EXECUTAMOS O MOCK_REPO
    with patch('src.databases.postgres.repository.catalog_repository.CatalogRepository.add_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Perfume incluido na base de dados!'}, 201)
        response = client.post('/catalogo/', data=payload, headers=headers)

    assert response.status_code == 201
    assert response.get_json() == {
        'sucess': True, 'message': 'Perfume incluido na base de dados!'}


def test_post_catalog_add_perfume_with_invalid_token_return_401_return_dict(client, non_admin_token):
    headers = {
        'Authorization': f'Bearer {non_admin_token}'
    }

    payload = {
        'perfume': 'MOCKADO',
        'ml': 999,
        'tipo': 'EDP',
        'preco': '999.99',
        'tags': 'mock_1, mock_2'
    }

    response = client.post('/catalogo/', data=payload, headers=headers)

    assert response.status_code == 401
    assert response.get_json() == {
        'sucess': False, 'message': f'Você não tem permissão para executar isso'}


def test_post_delete_perfume_with_valid_token_return_200_return_dict(client, product, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.databases.postgres.repository.catalog_repository.CatalogRepository.delete_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Item deletado com sucesso!'}, 200)
        response = client.post(
            f'/catalogo/deletar-perfume/{product.id}', headers=headers)

    assert response.status_code == 200
    assert response.get_json() == {'sucess': True,
                                   'message': 'Item deletado com sucesso!'}


def test_post_delete_perfume_with_invalid_token_return_401_return_dict(client, product, non_admin_token):
    headers = {
        'Authorization': f'Bearer {non_admin_token}'
    }

    with patch('src.databases.postgres.repository.catalog_repository.CatalogRepository.delete_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Item deletado com sucesso!'}, 200)
        response = client.post(
            f'/catalogo/deletar-perfume/{product.id}', headers=headers)

    assert response.status_code == 401
    assert response.get_json() == {'sucess': False,
                                   'message': 'Você não tem permissão para executar isso'}


def test_post_login_add_new_user_with_valid_credentials_return_201_content_type_json(client):
    payload = {
        'email': 'MOCKADO@email.com',
        'password': 'mock123@',
        'user': 'customer',
        'nome': 'John Doe',
        'cpf': '57230621070'
    }

    with patch('src.databases.postgres.repository.user_repository.UserRepository.add_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Login criado com sucesso!'}, 201)
        response = client.post('/login/create', json=payload)

    assert response.status_code == 201
    assert response.content_type == 'application/json'


def test_post_login_add_new_user_with_invalid_credentials_return_400_content_type_json(client):
    payload = {
        'email': 'MOCKADO',
        'password': 'mock123@',
        'user': 'customer',
        'nome': 'John Doe',
        'cpf': '57230621070'
    }
    response = client.post('/login/create', json=payload)

    assert response.status_code == 400
    assert response.content_type == 'application/json'


def test_post_login_make_login_return_200_return_dict(client, user):
    payload = {
        'email': 'MOCKADO@email.com',
        'password': 'mock123@'
    }

    with patch('src.databases.postgres.repository.user_repository.UserRepository.get_item') as mock_repo, \
            patch('src.services.security.bcrypt.bcrypt_handle.BcryptHandle.check_content') as mock_bcrypt, \
            patch('src.services.security.jwt.jwt_handle.JwtHandle.gen_token') as mock_jwt:

        mock_repo.return_value = user

        mock_bcrypt.return_value = True
        mock_jwt.return_value = 'MOCKjwt'

        response = client.post('/login/', json=payload)

        assert response.status_code == 200
        assert response.get_json() == {
            'sucess': True, 'message': 'Login Efetuado com sucesso', 'access_token': 'MOCKjwt'}


def test_post_login_make_login_using_id_return_200_return_dict(client, user):
    payload = {
        'password': 'mock123@'
    }

    with patch('src.databases.postgres.repository.user_repository.UserRepository.get_item') as mock_repo, \
            patch('src.services.security.bcrypt.bcrypt_handle.BcryptHandle.check_content') as mock_bcrypt, \
            patch('src.services.security.jwt.jwt_handle.JwtHandle.gen_token') as mock_jwt:

        mock_repo.return_value = user

        mock_bcrypt.return_value = True
        mock_jwt.return_value = 'MOCKjwt'

        response = client.post(
            f'/login/{mock_repo.return_value.id}', json=payload)

        assert response.status_code == 200
        assert response.get_json() == {
            'sucess': True, 'message': 'Login Efetuado com sucesso', 'access_token': 'MOCKjwt'}
