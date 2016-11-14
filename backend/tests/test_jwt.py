import unittest
from base64 import b64encode

import time

from jwt import JWT, JWTToken, JWTValidationError


class JWTTestCase(unittest.TestCase):

    def test_is_valid_false_bad_expire_time(self):
        token = JWT.create_token("test@email.com", "movie:read")
        jwt_token = JWTToken(token)
        jwt_token.parsed_payload["exp"] = int(time.time()) - 10
        try:
            jwt_token.is_valid()
        except JWTValidationError as exc:
            raised = True
            message = exc.message

        self.assertTrue(raised)
        self.assertEqual("Token expired", message)

    def test_is_valid_false_bad_signature(self):
        token = JWT.create_token("test@email.com", "movie:read")
        jwt_token = JWTToken(token)
        jwt_token.signature = "bad_signature"
        try:
            jwt_token.is_valid()
        except JWTValidationError as exc:
            raised = True
            message = exc.message

        self.assertTrue(raised)
        self.assertEqual("Invalid token!", message)

    def test_is_valid_against_scopes_false(self):
        token = JWT.create_token("test@email.com", "movie:read")
        jwt_token = JWTToken(token)
        try:
            jwt_token.has_permissions("movie:delete")
        except JWTValidationError as exc:
            raised = True
            message = exc.message

        self.assertTrue(raised)
        self.assertEqual("Permission denied for movie:delete", message)

    def test_is_valid_against_scopes_true(self):
        token = JWT.create_token("test@email.com", "movie:read")
        jwt_token = JWTToken(token)
        self.assertTrue(jwt_token.has_permissions("movie:read"))

    def test_is_valid_parse_failed_invalid_token(self):
        token = "not_valid_token"
        try:
            JWTToken(token)
        except JWTValidationError as exc:
            raised = True
            message = exc.message
        self.assertTrue(raised)
        self.assertEqual("Invalid auth token", message)

    def test_is_valid_parse_failed_decode_failed(self):
        token = "not_valid.token.for_decode"
        try:
            JWTToken(token)
        except JWTValidationError as exc:
            raised = True
            message = exc.message
        self.assertTrue(raised)
        self.assertEqual("Cannot decode token", message)

    def test_is_valid_parse_failed_json_decode_failed(self):
        header = JWT.construct_header()
        payload = JWT.construct_payload("test@email.com", ["movie:read"])
        # invalidate payload
        payload += "string_for_json_invalidation"
        signature = JWT.construct_signature(header, payload)
        token = b64encode(header) + "." + b64encode(payload) + "." + signature
        try:
            JWTToken(token)
        except JWTValidationError as exc:
            raised = True
            message = exc.message
        self.assertTrue(raised)
        self.assertEqual("Cannot load data from decoded token", message)
