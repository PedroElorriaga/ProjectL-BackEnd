from flask import Blueprint, jsonify, request
from src.services.http_types.http_requests import HttpRequest
from src.composers.catalog.catalog_composer import catalog_composer
from src.services.security.jwt.jwt_handle import token_required
from werkzeug.exceptions import Unauthorized
from src.services.image_uploader.cloudinary_handle import CloudinaryHandle

catalog_route = Blueprint('catalogo', __name__)


@catalog_route.route('/', defaults={'id_perfume': None}, methods=['GET'])
@catalog_route.route('/<int:id_perfume>', methods=['GET'])
def get_catalog(id_perfume: int | None = None) -> jsonify:
    catalog_repo = catalog_composer()

    if id_perfume:
        response = catalog_repo.get_perfume(id_perfume)
    elif len(request.args) > 0:
        response = catalog_repo.get_filtered_perfumes({
            'perfume': request.args.get('perfume'),
            'tipo': request.args.get('tipo'),
            'preco': request.args.get('preco', type=float),
            'tags_string': request.args.get('tags')
        })
    else:
        response = catalog_repo.get_perfume()

    return jsonify(response.body.model_dump()), response.status


@catalog_route.route('/', methods=['POST'])
@token_required
def add_perfume(user_token_information: tuple) -> jsonify:
    text_data = request.form.to_dict()
    image_file = request.files.get('imagem_url')
    image_url = None

    processed_body = {
        'perfume': text_data.get('perfume'),
        'ml': int(text_data.get('ml', 0)),
        'tipo': text_data.get('tipo'),
        'preco': float(text_data.get('preco', 0)),
        'tags': text_data.get('tags').split(','),
    }

    if image_file:
        cloudirary_handle = CloudinaryHandle()
        image_url = cloudirary_handle.upload_image(image_file)
        processed_body['imagem_url'] = image_url

    http_request = HttpRequest(processed_body)
    catalog_repo = catalog_composer()

    response = catalog_repo.add_new_perfume(
        http_request.body, user_token_information)

    return jsonify(response.body.model_dump()), response.status


@catalog_route.route('/deletar-perfume/<int:id_perfume>', methods=['POST'])
@token_required
def delete_perfume(user_token_information: tuple, id_perfume: int) -> jsonify:
    catalog_repo = catalog_composer()

    response = catalog_repo.delete_perfume(id_perfume, user_token_information)

    return jsonify(response.body.model_dump()), response.status


@catalog_route.route('/atualizar-perfume/<int:id_perfume>', methods=['POST'])
@token_required
def update_perfume(user_token_information: tuple, id_perfume: int) -> jsonify:
    http_request = HttpRequest(request.json)
    catalog_repo = catalog_composer()

    response = catalog_repo.patch_perfume(
        id_perfume, http_request.body, user_token_information)

    return jsonify(response.body.model_dump()), response.status


@catalog_route.errorhandler(Unauthorized)
def unauthorized_error(error) -> jsonify:
    # MANIPULA OS ERROS Unauthorized
    return jsonify({'sucess': False, 'message': error.description}), 401
