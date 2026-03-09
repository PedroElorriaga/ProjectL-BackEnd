from flask import Blueprint, jsonify, request
from src.shared.http_types.http_requests import HttpRequest
from src.modules.login.composers.login_composer import login_composer
from src.services.security.rate_limiter.rate_limiter import rate_limiter


login_route = Blueprint('login', __name__)


@login_route.route('/', defaults={'id_credential': None}, methods=['POST'])
@login_route.route('/<int:id_credential>', methods=['POST'])
@rate_limiter.limit(max_requests=5, window_seconds=60)
def make_login(id_credential: int | None = None) -> jsonify:
    http_request = HttpRequest(request.json)
    login_repo = login_composer()

    response = login_repo.get_login_credentials(
        http_request.body, id_credential)

    if response.status != 200:
        return jsonify(response.body.model_dump()), response.status

    return jsonify(response.body.model_dump()), response.status
