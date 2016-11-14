from functools import wraps

from backend.jwt import JWTValidationError, JWTToken
from backend.utils.helpers import json_response


def ensure_permissions(*permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(handler, *args, **kwargs):
            auth_header = handler.request.headers["Authorization"]
            if auth_header == "null":
                # no header
                json_response(handler, {"message": "You didn't provide authorization header"}, 401)
                return
            try:
                # trying to get token from `Bearer <token>` string
                token = auth_header.split(" ")[1]
            except IndexError:
                json_response(handler, {"message": "Invalid authorization header"}, 401)
                return
            try:
                # JWT validation
                jwt_token = JWTToken(token)
                jwt_token.is_valid()
                jwt_token.is_valid_against_scopes(*permissions)
                return func(handler, *args, **kwargs)
            except JWTValidationError as exc:
                json_response(handler, {"message": exc.message}, 401)

        return wrapper
    return decorator
