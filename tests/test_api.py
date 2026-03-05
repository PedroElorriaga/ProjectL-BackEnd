import pytest
import os
import jwt
from app import create_app
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from src.shared.http_types.http_response import HttpResponse
from src.modules.catalog.dtos.catalog_dto import CatalogUpdatePerfumeRequestDTO

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


def test_get_catalog_return_200_return_list(client):
    response = client.get('/catalogo/')

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data['message'], list)


def test_get_catalog_return_204_json_return_dict(client):
    with patch('src.modules.catalog.repositories.catalog_repository.CatalogRepository.get_all_itens') as mock_repo:
        mock_repo.return_value.itens = []
        mock_repo.return_value.response = HttpResponse(
            {'sucess': True, 'message': []}, 200)
        response = client.get('/catalogo/')

    assert response.status_code == mock_repo.return_value.response.status
    assert response.get_json() == mock_repo.return_value.response.body


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
    with patch('src.modules.catalog.repositories.catalog_repository.CatalogRepository.add_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Perfume incluido na base de dados!'}, 201)
        response = client.post('/catalogo/', data=payload, headers=headers)

    assert response.status_code == mock_repo.return_value.status
    assert response.get_json() == mock_repo.return_value.body


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


def test_delete_delete_perfume_with_valid_token_return_200_return_dict(client, product, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.catalog.repositories.catalog_repository.CatalogRepository.delete_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Item deletado com sucesso!'}, 200)
        response = client.delete(
            f'/catalogo/deletar-perfume/{product.id}', headers=headers)

    assert response.status_code == mock_repo.return_value.status
    assert response.get_json() == mock_repo.return_value.body


def test_delete_delete_perfume_with_invalid_token_return_401_return_dict(client, product, non_admin_token):
    headers = {
        'Authorization': f'Bearer {non_admin_token}'
    }

    with patch('src.modules.catalog.repositories.catalog_repository.CatalogRepository.delete_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': False, 'message': 'Você não tem permissão para executar isso'}, 401)
        response = client.delete(
            f'/catalogo/deletar-perfume/{product.id}', headers=headers)

    assert response.status_code == mock_repo.return_value.status
    assert response.get_json() == mock_repo.return_value.body


def test_put_update_perfume_with_valid_token_return_200_return_dict(client, product, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    payload = {
        'perfume': 'atualizado',
        'ml': 100,
        'preco': 299.99,
        'tipo': 'EDP',
        'tags': ['MOCK', 'ADO']
    }

    with patch('src.modules.catalog.repositories.catalog_repository.CatalogRepository.patch_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Item atualizado com sucesso!'}, 200)
        response = client.put(
            f'/catalogo/atualizar-perfume/{product.id}', json=payload, headers=headers)

        mock_repo.assert_called_once_with(
            product.id, CatalogUpdatePerfumeRequestDTO(**payload))

    assert response.status_code == mock_repo.return_value.status
    assert response.get_json() == mock_repo.return_value.body


def test_put_update_perfume_with_invalid_token_return_401_return_dict(client, product, non_admin_token):
    headers = {
        'Authorization': f'Bearer {non_admin_token}'
    }

    payload = {
        'perfume': 'atualizado',
        'ml': 100,
        'preco': 299.99,
        'tipo': 'EDP',
        'tags': ['MOCK', 'ADO']
    }

    with patch('src.modules.catalog.repositories.catalog_repository.CatalogRepository.patch_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': False, 'message': 'Você não tem permissão para executar isso'}, 401)
        response = client.put(
            f'/catalogo/atualizar-perfume/{product.id}', json=payload, headers=headers)

        mock_repo.assert_not_called()

    assert response.status_code == mock_repo.return_value.status
    assert response.get_json() == mock_repo.return_value.body


def test_post_login_create_new_user_with_valid_credentials_return_201_content_type_json(client):
    payload = {
        'email': 'MOCKADO@email.com',
        'senha': 'mock123@',
        'tipo_usuario': 'customer',
        'nome': 'John Doe',
        'cpf': '57230621070'
    }

    with patch('src.modules.users.repositories.user_repository.UserRepository.create_new_item') as mock_repo:
        mock_repo.return_value = HttpResponse(
            {'sucess': True, 'message': 'Usuário criado com sucesso!'}, 201)
        response = client.post('/usuario/criar', json=payload)

    assert response.status_code == mock_repo.return_value.status
    assert response.content_type == 'application/json'


def test_post_login_create_new_user_with_invalid_email_return_400_content_type_json_return_dict(client):
    payload = {
        'email': 'MOCKADO',
        'senha': 'mock123@',
        'tipo_usuario': 'customer',
        'nome': 'John Doe',
        'cpf': '57230621070'
    }
    response = client.post('/usuario/criar', json=payload)

    assert response.status_code == 400
    assert response.content_type == 'application/json'
    assert response.get_json() == {
        'message': 'Email inválido', 'sucess': False}


def test_post_login_make_login_return_200_return_dict(client, user):
    payload = {
        'email': 'MOCKADO@email.com',
        'senha': 'mock123@'
    }

    with patch('src.modules.users.repositories.user_repository.UserRepository.get_item') as mock_repo, \
            patch('src.services.security.bcrypt.bcrypt_handle.BcryptHandle.check_content') as mock_bcrypt, \
            patch('src.services.security.jwt.jwt_handle.JwtHandle.gen_token') as mock_jwt:

        mock_bcrypt.return_value = True
        mock_jwt.return_value = 'MOCKjwt'
        mock_repo.return_value.item = user
        mock_repo.return_value.response = HttpResponse({
            'sucess': True, 'message': 'Login Efetuado com sucesso', 'access_token': mock_jwt.return_value}, 200)

        response = client.post('/login/', json=payload)

    assert response.status_code == mock_repo.return_value.response.status
    assert response.get_json() == mock_repo.return_value.response.body


def test_post_login_make_login_using_id_return_200_return_dict(client, user):
    payload = {
        'senha': 'mock123@'
    }

    with patch('src.modules.users.repositories.user_repository.UserRepository.get_item') as mock_repo, \
            patch('src.services.security.bcrypt.bcrypt_handle.BcryptHandle.check_content') as mock_bcrypt, \
            patch('src.services.security.jwt.jwt_handle.JwtHandle.gen_token') as mock_jwt:

        mock_bcrypt.return_value = True
        mock_jwt.return_value = 'MOCKjwt'
        mock_repo.return_value.item = user
        mock_repo.return_value.response = HttpResponse({
            'sucess': True, 'message': 'Login Efetuado com sucesso', 'access_token': mock_jwt.return_value}, 200)

        response = client.post(
            f'/login/{mock_repo.return_value.item.id}', json=payload)

    assert response.status_code == mock_repo.return_value.response.status
    assert response.get_json() == mock_repo.return_value.response.body


# =============================================================================
# SUPPLIER FIXTURES
# =============================================================================

@pytest.fixture
def supplier():
    mock_supplier = MagicMock()
    mock_supplier.fornecedor_id = 1
    mock_supplier.razao = 'Fornecedor Mock LTDA'
    mock_supplier.email = 'mock@fornecedor.com'
    mock_supplier.cnpj = '12345678000199'
    mock_supplier.numero_tel = '11999999999'
    mock_supplier.cep = '01310100'
    mock_supplier.rua = 'Rua Mock'
    mock_supplier.numero_endereco = 123
    mock_supplier.cidade = 'São Paulo'
    mock_supplier.uf = 'SP'
    mock_supplier.pais = 'Brasil'
    return mock_supplier


@pytest.fixture
def supplier_list():
    return [
        {
            'fornecedor_id': 1,
            'razao': 'Fornecedor A',
            'email': 'a@fornecedor.com',
            'cnpj': '12345678000199',
            'numero_tel': '11999999999',
            'cep': '01310100',
            'rua': 'Rua A',
            'numero_endereco': 100,
            'cidade': 'São Paulo',
            'uf': 'SP',
            'pais': 'Brasil'
        },
        {
            'fornecedor_id': 2,
            'razao': 'Fornecedor B',
            'email': 'b@fornecedor.com',
            'cnpj': '98765432000188',
            'numero_tel': '21888888888',
            'cep': '20040020',
            'rua': 'Rua B',
            'numero_endereco': 200,
            'cidade': 'Rio de Janeiro',
            'uf': 'RJ',
            'pais': 'Brasil'
        }
    ]


# =============================================================================
# GET /fornecedor/ - Get All Suppliers Tests
# =============================================================================

def test_get_all_suppliers_with_valid_admin_token_return_200(client, admin_token, supplier_list):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.get_all_itens') as mock_repo:
        mock_repo.return_value = supplier_list
        response = client.get('/fornecedor/', headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['sucess'] is True
    assert isinstance(data['message'], list)


def test_get_all_suppliers_with_non_admin_token_return_401(client, non_admin_token):
    headers = {
        'Authorization': f'Bearer {non_admin_token}'
    }

    response = client.get('/fornecedor/', headers=headers)

    assert response.status_code == 401
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Você não tem permissão para executar isso'


def test_get_all_suppliers_empty_list_return_204(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.get_all_itens') as mock_repo:
        mock_repo.return_value = []
        response = client.get('/fornecedor/', headers=headers)

    assert response.status_code == 204


def test_get_all_suppliers_with_invalid_token_return_401(client):
    headers = {
        'Authorization': 'Bearer invalid_token_here'
    }

    response = client.get('/fornecedor/', headers=headers)

    assert response.status_code == 401


# =============================================================================
# GET /fornecedor/<id> - Get Supplier by ID Tests
# =============================================================================

def test_get_supplier_by_id_with_valid_admin_token_return_200(client, admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.get_item_by_id') as mock_repo:
        mock_repo.return_value = {
            'fornecedor_id': supplier.fornecedor_id,
            'razao': supplier.razao,
            'email': supplier.email,
            'cnpj': supplier.cnpj,
            'numero_tel': supplier.numero_tel,
            'cep': supplier.cep,
            'rua': supplier.rua,
            'numero_endereco': supplier.numero_endereco,
            'cidade': supplier.cidade,
            'uf': supplier.uf,
            'pais': supplier.pais
        }
        response = client.get(
            f'/fornecedor/{supplier.fornecedor_id}', headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['sucess'] is True


def test_get_supplier_by_id_with_non_admin_token_return_401(client, non_admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {non_admin_token}'
    }

    response = client.get(
        f'/fornecedor/{supplier.fornecedor_id}', headers=headers)

    assert response.status_code == 401
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Você não tem permissão para executar isso'


def test_get_supplier_by_id_not_found_return_204(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.get_item_by_id') as mock_repo:
        mock_repo.return_value = None
        response = client.get('/fornecedor/9999', headers=headers)

    assert response.status_code == 204


# =============================================================================
# POST /fornecedor/criar - Create Supplier Tests
# =============================================================================

def test_create_supplier_with_valid_admin_token_return_201(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Novo Fornecedor LTDA',
        'email': 'novo@fornecedor.com',
        'cnpj': '11223344000155',
        'numero_tel': '11912345678',
        'cep': '01310100',
        'rua': 'Rua Nova',
        'numero_endereco': 456,
        'cidade': 'São Paulo',
        'uf': 'SP',
        'pais': 'Brasil'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.create_new_item') as mock_repo:
        mock_repo.return_value = None
        response = client.post('/fornecedor/criar',
                               json=payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data['sucess'] is True
    assert data['message'] == 'Fornecedor incluido com sucesso'


def test_create_supplier_with_non_admin_token_return_401(client, non_admin_token):
    headers = {
        'Authorization': f'Bearer {non_admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Novo Fornecedor LTDA',
        'email': 'novo@fornecedor.com'
    }

    response = client.post('/fornecedor/criar', json=payload, headers=headers)

    assert response.status_code == 401
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Você não tem permissão para executar isso'


def test_create_supplier_with_minimal_data_return_201(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor Minimo LTDA'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.create_new_item') as mock_repo:
        mock_repo.return_value = None
        response = client.post('/fornecedor/criar',
                               json=payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data['sucess'] is True


def test_create_supplier_without_razao_return_500(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'email': 'sem_razao@fornecedor.com'
    }

    response = client.post('/fornecedor/criar', json=payload, headers=headers)

    assert response.status_code == 500
    data = response.get_json()
    assert data['sucess'] is False


def test_create_supplier_with_invalid_email_return_500(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor Invalido',
        'email': 'email_invalido'
    }

    response = client.post('/fornecedor/criar', json=payload, headers=headers)

    assert response.status_code == 500
    data = response.get_json()
    assert data['sucess'] is False


def test_create_supplier_with_full_address_return_201(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor Completo S.A.',
        'email': 'completo@fornecedor.com.br',
        'cnpj': '99887766000144',
        'numero_tel': '1133334444',
        'cep': '04538133',
        'rua': 'Avenida Faria Lima',
        'numero_endereco': 1000,
        'cidade': 'São Paulo',
        'uf': 'SP',
        'pais': 'Brasil'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.create_new_item') as mock_repo:
        mock_repo.return_value = None
        response = client.post('/fornecedor/criar',
                               json=payload, headers=headers)

    assert response.status_code == 201
    data = response.get_json()
    assert data['sucess'] is True
    assert data['message'] == 'Fornecedor incluido com sucesso'


# =============================================================================
# PUT /fornecedor/<id>/atualizar - Update Supplier Tests
# =============================================================================

def test_update_supplier_with_valid_admin_token_return_200(client, admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor Atualizado LTDA',
        'email': 'atualizado@fornecedor.com'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.update_item_by_id') as mock_repo:
        mock_repo.return_value = None
        response = client.put(
            f'/fornecedor/{supplier.fornecedor_id}/atualizar',
            json=payload,
            headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()
    assert data['sucess'] is True
    assert data['message'] == 'Fornecedor atualizado com sucesso'


def test_update_supplier_with_non_admin_token_return_401(client, non_admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {non_admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor Atualizado LTDA'
    }

    response = client.put(
        f'/fornecedor/{supplier.fornecedor_id}/atualizar',
        json=payload,
        headers=headers
    )

    assert response.status_code == 401
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Você não tem permissão para executar isso'


def test_update_supplier_not_found_return_404(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor Inexistente'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.update_item_by_id') as mock_repo:
        mock_repo.side_effect = FileNotFoundError('Item não foi encontrado')
        response = client.put('/fornecedor/9999/atualizar',
                              json=payload, headers=headers)

    assert response.status_code == 404
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Fornecedor não encontrado'


def test_update_supplier_partial_update_return_200(client, admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'cidade': 'Campinas'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.update_item_by_id') as mock_repo:
        mock_repo.return_value = None
        response = client.put(
            f'/fornecedor/{supplier.fornecedor_id}/atualizar',
            json=payload,
            headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()
    assert data['sucess'] is True


def test_update_supplier_with_invalid_email_return_500(client, admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'email': 'email_invalido'
    }

    response = client.put(
        f'/fornecedor/{supplier.fornecedor_id}/atualizar',
        json=payload,
        headers=headers
    )

    assert response.status_code == 500
    data = response.get_json()
    assert data['sucess'] is False


def test_update_supplier_all_fields_return_200(client, admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor Totalmente Atualizado',
        'email': 'novo_email@fornecedor.com',
        'cnpj': '11111111000111',
        'numero_tel': '11900001111',
        'cep': '05000000',
        'rua': 'Nova Rua',
        'numero_endereco': 999,
        'cidade': 'Nova Cidade',
        'uf': 'RJ',
        'pais': 'Brasil'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.update_item_by_id') as mock_repo:
        mock_repo.return_value = None
        response = client.put(
            f'/fornecedor/{supplier.fornecedor_id}/atualizar',
            json=payload,
            headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()
    assert data['sucess'] is True


# =============================================================================
# DELETE /fornecedor/<id>/deletar - Delete Supplier Tests
# =============================================================================

def test_delete_supplier_with_valid_admin_token_return_200(client, admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.delete_item_by_id') as mock_repo:
        mock_repo.return_value = None
        response = client.delete(
            f'/fornecedor/{supplier.fornecedor_id}/deletar',
            headers=headers
        )

    assert response.status_code == 200
    data = response.get_json()
    assert data['sucess'] is True
    assert data['message'] == 'Fornecedor deletado com sucesso'


def test_delete_supplier_with_non_admin_token_return_401(client, non_admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {non_admin_token}'
    }

    response = client.delete(
        f'/fornecedor/{supplier.fornecedor_id}/deletar',
        headers=headers
    )

    assert response.status_code == 401
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Você não tem permissão para executar isso'


def test_delete_supplier_not_found_return_404(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.delete_item_by_id') as mock_repo:
        mock_repo.side_effect = FileNotFoundError('Item não foi encontrado')
        response = client.delete('/fornecedor/9999/deletar', headers=headers)

    assert response.status_code == 404
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Fornecedor não encontrado'


# =============================================================================
# Supplier Error Handling Tests
# =============================================================================

def test_get_supplier_repository_exception_return_500(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.get_all_itens') as mock_repo:
        mock_repo.side_effect = Exception('Database connection error')
        response = client.get('/fornecedor/', headers=headers)

    assert response.status_code == 500
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Ocorreu algum erro inesperado'


def test_create_supplier_repository_exception_return_500(client, admin_token):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor com Erro'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.create_new_item') as mock_repo:
        mock_repo.side_effect = Exception('Database insert error')
        response = client.post('/fornecedor/criar',
                               json=payload, headers=headers)

    assert response.status_code == 500
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Ocorreu algum erro inesperado'


def test_update_supplier_repository_exception_return_500(client, admin_token, supplier):
    headers = {
        'Authorization': f'Bearer {admin_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'razao': 'Fornecedor com Erro'
    }

    with patch('src.modules.suppliers.repositories.supplier_repository.SupplierRepository.update_item_by_id') as mock_repo:
        mock_repo.side_effect = Exception('Database update error')
        response = client.put(
            f'/fornecedor/{supplier.fornecedor_id}/atualizar',
            json=payload,
            headers=headers
        )

    assert response.status_code == 500
    data = response.get_json()
    assert data['sucess'] is False
    assert data['message'] == 'Ocorreu algum erro inesperado'
