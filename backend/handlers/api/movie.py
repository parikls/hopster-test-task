import webapp2
from google.appengine.ext import db

from backend.models import Movie
from backend.utils.decorators import ensure_permissions
from backend.utils.helpers import json_response


class MovieListHandler(webapp2.RequestHandler):

    @ensure_permissions("movie:read")
    def get(self):
        movies = db.GqlQuery(
            "SELECT * FROM Movie ORDER BY add_timestamp DESC"
        )
        movie_list = [movie.to_dict() for movie in movies]
        json_response(self, data=movie_list, status=200)

    @ensure_permissions("movie:create")
    def post(self):
        name = self.request.get("name")
        description = self.request.get("description")

        if not (name and description):
            json_response(self, {"message": "Name and description fields must be filled"}, status=400)
            return

        movie = Movie(name=name, description=description)
        movie.put()

        json_response(self, data=movie.to_dict(), status=201)


class MovieDetailsHandler(webapp2.RequestHandler):

    @ensure_permissions("movie:read")
    def get(self, movie_id):
        try:
            movie = Movie.get_by_id(int(movie_id))
        except ValueError:
            json_response(self, {"message": "invalid movie id"}, status=400)
            return

        json_response(self, movie.to_dict(), status=200)

    @ensure_permissions("movie:update")
    def post(self, movie_id):
        try:
            movie = Movie.get_by_id(int(movie_id))
        except ValueError:
            json_response(self, {"message": "invalid movie id"}, status=400)
            return

        name = self.request.get("name")
        description = self.request.get("description")

        if not (name and description):
            json_response(self, {"message": "You didn't send any fields for update"}, status=400)
            return

        movie.name = name
        movie.description = description
        movie.put()
        json_response(self, status=204)

    @ensure_permissions("movie:delete")
    def delete(self, movie_id):

        try:
            movie = Movie.get_by_id(int(movie_id))
        except ValueError:
            json_response(self, {"message": "invalid movie id"}, status=400)
            return

        movie.delete()
        self.response.status = 204
