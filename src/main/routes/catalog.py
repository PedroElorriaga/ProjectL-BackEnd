from flask import Blueprint, jsonify, request
from src.services.http_types.http_requests import HttpRequest
from src.composers.catalog.catalog_composer import catalog_composer
from src.services.security.jwt.jwt_handle import token_required
from werkzeug.exceptions import Unauthorized

catalog_route = Blueprint('catalogo', __name__)


@catalog_route.route('/', methods=['GET'])
def get_catalog() -> jsonify:
    catalog_repo = catalog_composer()

    response = catalog_repo.get_all_perfume()

    return jsonify(response.body), response.status


@catalog_route.route('/<int:id_perfume>', methods=['GET'])
def get_one_perfume(id_perfume: int) -> jsonify:
    catalog_repo = catalog_composer()

    response = catalog_repo.get_perfume(id_perfume)

    return jsonify(response.body), response.status


@catalog_route.route('/', methods=['POST'])
@token_required
def add_perfume(user_token_information: tuple) -> jsonify:
    http_request = HttpRequest(request.json)
    catalog_repo = catalog_composer()

    response = catalog_repo.add_new_perfume(
        http_request.body, user_token_information)

    return jsonify(response.body), response.status


@catalog_route.route('/deletar-perfume/<int:id_perfume>', methods=['POST'])
@token_required
def delete_perfume(user_token_information: tuple, id_perfume: int) -> jsonify:
    catalog_repo = catalog_composer()

    response = catalog_repo.delete_perfume(id_perfume, user_token_information)

    return jsonify(response.body), response.status


@catalog_route.route('/atualizar-perfume/<int:id_perfume>', methods=['POST'])
@token_required
def update_perfume(user_token_information: tuple, id_perfume: int) -> jsonify:
    http_request = HttpRequest(request.json)
    catalog_repo = catalog_composer()
    print(id_perfume)

    response = catalog_repo.patch_perfume(
        id_perfume, http_request.body, user_token_information)

    return jsonify(response.body), response.status


@catalog_route.errorhandler(Unauthorized)
def unauthorized_error(error) -> jsonify:
    # MANIPULA OS ERROS Unauthorized
    return jsonify({'sucess': False, 'message': error.description}), 401
