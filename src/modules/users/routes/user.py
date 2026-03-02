from flask import Blueprint, jsonify, request
from src.services.http_types.http_requests import HttpRequest
from src.modules.users.composers.user_composer import user_composer


user_route = Blueprint('usuario', __name__)


@user_route.route('/criar', methods=['POST'])
def create_user() -> jsonify:
    http_request = HttpRequest(request.json)
    user_repo = user_composer()

    response = user_repo.create_user(http_request.body)

    return jsonify(response.body.model_dump()), response.status
