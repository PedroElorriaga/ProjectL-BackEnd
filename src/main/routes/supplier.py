from flask import Blueprint, jsonify
from src.composers.suppliers.supplier_composer import supplier_composer
from src.services.security.jwt.jwt_handle import token_required


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

    return jsonify(response.body.model_dump(), response.status)
