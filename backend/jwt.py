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


class JWTToken:

    def __init__(self, token):
        self.token = token
        self.decoded_header = None
        self.decoded_payload = None
        self.parsed_header = None
        self.parsed_payload = None
        self.signature = None
        self._parse()

    def is_valid(self):
        if self.parsed_payload.get("exp", 0) < int(time.time()):
            raise JWTValidationError(message="Token expired")

        if JWT.construct_signature(self.decoded_header, self.decoded_payload) != self.signature:
            raise JWTValidationError("Invalid token!")

        return True

    def is_valid_against_scopes(self, scopes):

        for scope in scopes:
            if scope not in self.parsed_payload["scopes"]:
                raise JWTValidationError("Permission denied for {}".format(scope))
        return True

    def _parse(self):
        try:
            header, payload, signature = self.token.split(".")
        except ValueError:
            raise JWTValidationError(message="Invalid auth token")
        try:
            self.decoded_header, self.decoded_payload = b64decode(header), b64decode(payload)
        except TypeError:
            raise JWTValidationError(message="Cannot decode token")
        try:
            self.parsed_header, self.parsed_payload = json.loads(self.decoded_header), json.loads(self.decoded_payload)
        except ValueError:
            raise JWTValidationError(message="Cannot load data from decoded token ")

        self.signature = signature


class JWT:

    """
    JSON Web Token implementation. Only SHA256 is supported.
    """

    def __new__(cls, *args, **kwargs):
        raise NotImplemented("Use classmethods instead of JWT Instance creation")

    @classmethod
    def create_token(cls, email, scopes):
        """
        Creates token using user email and permission scopes
        :param: email: str
        :param: scopes: list
        """
        header = cls.construct_header()
        payload = cls.construct_claim(email, scopes)
        signature = cls.construct_signature(header, payload)
        return b64encode(header) + "." + b64encode(payload) + "." + signature

    @classmethod
    def construct_header(cls):

        return json.dumps({
            "typ": "JWT",
            "alg": "HS256"
        })

    @classmethod
    def construct_claim(cls, email, scopes):

        return json.dumps(
            {
                "iss": "hopster",
                "exp": int(time.time()) + JWT_SECONDS_EXPIRY_TIME,
                "jti": email,
                "scopes": scopes
            }
        )

    @classmethod
    def construct_signature(cls, header, payload):
        encoded_string = urlsafe_b64encode(header) + "." + urlsafe_b64encode(payload)
        signature = b64encode(hmac.new(JWT_SECRET, encoded_string, hashlib.sha256).hexdigest())
        return signature
