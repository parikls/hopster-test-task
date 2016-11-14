import logging
from functools import wraps

from backend.jwt import JWTValidationError, JWTToken
from backend.utils.helpers import json_response


def ensure_permissions(*permissions):
    """
    Decorator which ensures that user has correct
    permissions based on provided JWT in header
    :param permissions: str
    """

    def decorator(func):
        @wraps(func)
        def wrapper(handler, *args, **kwargs):
            auth_header = handler.request.headers["Authorization"]
            if auth_header == "null":
                # no header
                logging.debug("Authorization header is blank. path_info: {}".format(handler.request.path_info))
                json_response(handler, {"message": "You didn't provide authorization header"}, status=401)
                return
            try:
                # trying to get token from `Bearer <token>` string
                token = auth_header.split(" ")[1]
            except IndexError:
                logging.warn("Cannot parse Authorization header. header: {}. path_info: {}".format(
                    auth_header, handler.request.path_info))
                json_response(handler, {"message": "Invalid authorization header"}, status=401)
                return

            # Start JWT validation
            try:
                # parsing
                jwt_token = JWTToken(token)
            except JWTValidationError as exc:
                logging.warn("Cannot parse Authorization header. header: {}. path_info: {}".format(
                    auth_header, handler.request.path_info))
                json_response(handler, {"message": exc.message}, status=401)
                return

            try:
                # validation
                jwt_token.is_valid()
            except JWTValidationError as exc:
                logging.warn("JWT Token is not valid. header: {}. path_info: {}".format(
                    auth_header, handler.request.path_info))
                json_response(handler, {"message": exc.message}, status=401)
                return

            try:
                # permissions
                jwt_token.has_permissions(*permissions)
                return func(handler, *args, **kwargs)
            except JWTValidationError as exc:
                logging.warn("Attempt to access object without permissions. header: {}. path_info: {}".format(
                    auth_header, handler.request.path_info))
                json_response(handler, {"message": exc.message}, status=401)

        return wrapper

    return decorator
