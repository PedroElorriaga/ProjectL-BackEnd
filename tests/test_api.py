import pytest
import os
import jwt
from app import create_app
from dotenv import load_dotenv
from unittest.mock import patch
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


def test_get_catalog_return_200_content_type_json_return_list(client):
    response = client.get('/catalogo/')

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert isinstance(data['message'], list)


def test_post_catalog_add_perfume_with_valid_token_return_201_return_dict(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    payload = {
        'perfume': 'MOCKADO',
        'ml': 999,
        'tipo': 'EDP',
        'preco': '999.99',
        'tags': ['PY', 'TEST']
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
        'tags': ['PY', 'TEST']
    }

    response = client.post('/catalogo/', data=payload, headers=headers)

    assert response.status_code == 401
    assert response.get_json() == {
        'sucess': False, 'message': f'Você não tem permissão para executar isso'}
