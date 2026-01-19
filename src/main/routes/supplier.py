from flask import Blueprint, redirect, jsonify
from src.composers.suppliers.supplier_composer import supplier_composer


supplier_route = Blueprint('fornecedor', __name__)


@supplier_route.route('/')
def get_suppliers() -> jsonify:
    supplier_repo = supplier_composer()

    response = supplier_repo.get_all_suppliers()
    print(response.body)

    return jsonify(response.body.model_dump(), response.status)
