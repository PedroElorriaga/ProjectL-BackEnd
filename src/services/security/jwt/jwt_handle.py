import jwt
from datetime import datetime, timezone, timedelta
from flask import current_app, request
from functools import wraps
from werkzeug.exceptions import Unauthorized


class JwtHandle:

    @staticmethod
    def gen_token(user_id: int, user_role: str) -> str:
        expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)

        token = jwt.encode({
            'public_id': user_id, 'user_role': user_role, 'exp': expiration_time
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return token


def token_required(f) -> tuple:
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            raise Unauthorized('Token is missing')

        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            user_id = data.get('public_id')
            user_role = data.get('user_role')

            user_information = (user_id, user_role)

        except jwt.ExpiredSignatureError:
            raise Unauthorized('Token is expired')
        except jwt.InvalidTokenError:
            raise Unauthorized('Invalid token authentication')
        except Exception:
            raise Unauthorized('Ocorreu um erro interno ao processar o token')

        return f(user_information, *args, **kwargs)

    return decorated
