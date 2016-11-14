import logging
import webapp2
from google.appengine.ext import db

from backend.jwt import JWT
from backend.models import User
from backend.settings import JWT_DEFAULT_PERMISSIONS
from backend.utils.helpers import json_response


class LoginHandler(webapp2.RequestHandler):

    def post(self):

        email = self.request.get("email")
        password = self.request.get("password")

        logging.debug("LoginHandler. POST. email: {}".format(email))

        if not (email and password):
            logging.info("LoginHandler. POST. blank credentials")
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
        logging.info("LoginHandler. POST. login. invalid password. email: {}".format(user.email))
        json_response(self, {"message": "Invalid password"}, status=401)

    def _register(self, email, password):
        logging.debug("LoginHandler. POST. register. email: {}".format(email))
        new_user = User(email=email, password=password)
        new_user.put()
        self._set_token(new_user)

    def _set_token(self, user):
        logging.debug("LoginHandler. POST. set_token. email: {}".format(user.email))
        token = JWT.create_token(user.email, *JWT_DEFAULT_PERMISSIONS)
        self.response.headers["JWT"] = token
        self.response.status = 200
