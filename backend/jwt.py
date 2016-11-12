import hashlib
import hmac
import json
import time
from base64 import b64encode, b64decode, urlsafe_b64encode

from settings import JWT_SECONDS_EXPIRY_TIME, JWT_SECRET


class JWTValidationError(Exception):
    def __init__(self, message, *args, **kwargs):
        super(JWTValidationError, self).__init__(*args, **kwargs)
        self.message = message


class JWT:
    """
    JSON Web Token implementation. Only SHA256 is supported.
    """

    def __new__(cls, *args, **kwargs):
        raise NotImplemented("Use classmethods instead of JWT Instance creation")

    @classmethod
    def create_token(cls, email):
        """
        Creates token using user email
        """
        header = cls.__construct_header()
        payload = cls.__construct_auth_claim(email)
        signature = cls.__construct_signature(header, payload)
        return b64encode(header) + "." + b64encode(payload) + "." + signature

    @classmethod
    def verify_token(cls, token):
        """
        Check if token is valid
        Raises JWTValidationError if token is not valid
        """
        header, payload, signature = token.split(".")
        try:
            decoded_header, decoded_payload = b64decode(header), b64decode(payload)
        except TypeError:
            raise JWTValidationError(message="Cannot decode token")
        try:
            dict_header, dict_payload = json.loads(decoded_header), json.loads(decoded_payload)
        except ValueError:
            raise JWTValidationError(message="Cannot load data from decoded token ")

        if dict_payload.get("exp", 0) < int(time.time()):
            raise JWTValidationError(message="Token expired")

        if cls.__construct_signature(decoded_header, decoded_payload) != signature:
            raise JWTValidationError("Invalid token!")

    @classmethod
    def __construct_header(cls):

        return json.dumps({
            "typ": "JWT",
            "alg": "HS256"
        })

    @classmethod
    def __construct_auth_claim(cls, email):

        return json.dumps(
            {
                "iss": "hopster",
                "exp": int(time.time()) + JWT_SECONDS_EXPIRY_TIME,
                "name": email,
                "auth": True
            }
        )

    @classmethod
    def __construct_signature(cls, header, payload):
        encoded_string = urlsafe_b64encode(header) + "." + urlsafe_b64encode(payload)
        signature = b64encode(hmac.new(JWT_SECRET, encoded_string, hashlib.sha256).hexdigest())
        return signature
