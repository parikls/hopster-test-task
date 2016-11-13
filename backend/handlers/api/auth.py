import json
import logging

import webapp2
from google.appengine.ext import db

from jwt import JWT
from models import User
from settings import JWT_DEFAULT_SCOPES
from utils.helpers import json_response


class AuthException(Exception): pass


class LoginHandler(webapp2.RequestHandler):

    def post(self):

        email = self.request.get("email")
        password = self.request.get("password")

        if not (email and password):
            json_response(self, {"message": "Credentials cannot be blank"}, 400)
            return

        user = db.GqlQuery("SELECT * FROM User WHERE email=:1", email).get()

        if not user:
            # if no such user - register
            return self._register(email, password)

        # try to login
        return self._login(user, password)

    def _login(self, user, password):
        if user.password == password:
            # generate JWT for this user
            self._set_token(user)
            return
        json_response(self, {"message": "Invalid password"}, status=401)

    def _register(self, email, password):
        new_user = User(email=email, password=password)
        new_user.put()
        self._set_token(new_user)

    def _set_token(self, user):
        token = JWT.create_token(user.email, JWT_DEFAULT_SCOPES)
        self.response.headers["JWT"] = token
        self.response.status = 200


