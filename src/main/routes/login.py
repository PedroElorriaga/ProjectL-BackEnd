from flask import Blueprint, jsonify, request, make_response
from src.services.http_types.http_requests import HttpRequest
from src.composers.login.login_composer import login_composer


login_route = Blueprint('login', __name__)


@login_route.route('/create', methods=['POST'])
def add_login() -> jsonify:
    http_request = HttpRequest(request.json)
    login_repo = login_composer()

    response = login_repo.add_new_login(http_request.body)

    return jsonify(response.body), response.status


@login_route.route('/', defaults={'id_credential': None}, methods=['POST'])
@login_route.route('/<int:id_credential>', methods=['POST'])
def make_login(id_credential: int | None = None) -> make_response:
    http_request = HttpRequest(request.json)
    login_repo = login_composer()

    response = login_repo.get_login_credentials(
        http_request.body, id_credential)

    if response.status != 200:
        return jsonify(response.body), response.status

    http_response = make_response(response.body, response.status)
    http_response.set_cookie(
        'jwt_token',
        response.body.get('token'),
        httponly=True,
        # Impede que o JavaScript leia o cookie (protege contra XSS).
        secure=True  # Garante que o cookie só será enviado em HTTPS.
    )

    return http_response
