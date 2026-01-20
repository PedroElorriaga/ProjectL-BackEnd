from flask import Blueprint, jsonify, request
from src.composers.suppliers.supplier_composer import supplier_composer
from src.services.security.jwt.jwt_handle import token_required
from src.services.http_types.http_requests import HttpRequest


supplier_route = Blueprint('fornecedor', __name__)


@supplier_route.route('/', defaults={'id_supplier': None}, methods=['GET'])
@supplier_route.route('/<int:id_supplier>', methods=['GET'])
@token_required
def get_suppliers(user_token_information: tuple, id_supplier: int) -> jsonify:
    supplier_repo = supplier_composer()

    if id_supplier:
        response = supplier_repo.get_supplier(
            user_token_information, id_supplier)
    else:
        response = supplier_repo.get_supplier(user_token_information)

    return jsonify(response.body.model_dump()), response.status


@supplier_route.route('/criar', methods=['POST'])
@token_required
def create_new_supplier(user_token_information: tuple) -> jsonify:
    http_request = HttpRequest(request.json)
    supplier_repo = supplier_composer()

    response = supplier_repo.create_supplier(
        user_token_information, http_request.body)

    return jsonify(response.body.model_dump()), response.status


@supplier_route.route('/<int:id_supplier>/atualizar', methods=['PUT'])
@token_required
def update_supplier(user_token_information: tuple, id_supplier: int) -> jsonify:
    http_request = HttpRequest(request.json)
    supplier_repo = supplier_composer()

    response = supplier_repo.update_supplier(
        user_token_information, id_supplier, http_request.body)

    return jsonify(response.body.model_dump()), response.status


@supplier_route.route('/<int:id_supplier>/deletar', methods=['DELETE'])
@token_required
def delete_supplier(user_token_information: tuple, id_supplier: int) -> jsonify:
    supplier_repo = supplier_composer()

    response = supplier_repo.delete_supplier(
        user_token_information, id_supplier)

    return jsonify(response.body.model_dump()), response.status
