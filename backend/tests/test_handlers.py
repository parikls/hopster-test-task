import json
import unittest

from google.appengine.ext import testbed

import main
import webapp2
from backend.models import Movie, User


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.user = User(email="test@email.com", password="password")
        self.user.put()

    def tearDown(self):
        self.testbed.deactivate()


class TestAuthHandler(BaseTestCase):

    def setUp(self):
        super(TestAuthHandler, self).setUp()


    def test_login_email_blank(self):
        post_data = {"password": "fgkgjfdklgjkdfjgk"}
        request = webapp2.Request.blank("/api/auth/login/", POST=post_data)
        response = request.get_response(main.app)
        response_body = json.loads(response.body)
        self.assertEqual(400, response.status_int)
        self.assertEqual("Credentials cannot be blank", response_body["message"])

    def test_login_password_blank(self):
        post_data = {"password": "fgkgjfdklgjkdfjgk"}
        request = webapp2.Request.blank("/api/auth/login/", POST=post_data)
        response = request.get_response(main.app)
        response_body = json.loads(response.body)
        self.assertEqual(400, response.status_int)
        self.assertEqual("Credentials cannot be blank", response_body["message"])

    def test_login_invalid_password(self):
        post_data = {"email": "test@email.com", "password": "fgkgjfdklgjkdfjgk"}
        request = webapp2.Request.blank("/api/auth/login/", POST=post_data)
        response = request.get_response(main.app)
        response_body = json.loads(response.body)
        self.assertEqual(401, response.status_int)
        self.assertEqual("Invalid password", response_body["message"])

    def test_login_success(self):
        post_data = {"email": "test@email.com", "password": "password"}
        request = webapp2.Request.blank("/api/auth/login/", POST=post_data)
        response = request.get_response(main.app)
        headers = response.headers
        self.assertEqual(200, response.status_int)
        self.assertTrue("JWT" in headers)


class TestMovieHandler(BaseTestCase):

    def setUp(self):
        super(TestMovieHandler, self).setUp()
        # create several movies
        for i in range(3):
            movie = Movie(name="movie%i" % i, description="description%i" % i)
            movie.put()
            self.movie = movie.key()

        post_data = {"email": "test@email.com", "password": "password"}
        request = webapp2.Request.blank("/api/auth/login/", POST=post_data)
        response = request.get_response(main.app)
        self.jwt_token = response.headers["JWT"]

    def test_get_all_movies(self):
        request = webapp2.Request.blank("/api/movie/", headers={"Authorization": "Bearer {}".format(self.jwt_token)})
        response = request.get_response(main.app)
        movies = json.loads(response.body)

        self.assertEqual(3, len(movies))
        # check movies are present with correct ordering
        self.assertEqual("movie2", movies[0]["name"])
        self.assertEqual("movie1", movies[1]["name"])
        self.assertEqual("movie0", movies[2]["name"])

    def test_get_movie(self):
        request = webapp2.Request.blank("/api/movie/%i/" % self.movie.id(), headers={"Authorization": "Bearer {}".format(self.jwt_token)})
        response = request.get_response(main.app)
        movie = json.loads(response.body)

        # check movies are present with correct ordering
        self.assertEqual("movie2", movie["name"])

    def test_update_movie_success(self):
        pass

    def test_update_movie_invalid_id(self):
        pass

    def test_update_movie_no_fields_are_provided(self):
        pass

    def test_delete_movie_success(self):
        pass

    def test_delete_movie_invalid_id(self):
        pass

