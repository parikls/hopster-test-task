import logging
import webapp2
from google.appengine.ext import db

from backend.models import Movie
from backend.utils.decorators import ensure_permissions
from backend.utils.helpers import json_response


class MovieListHandler(webapp2.RequestHandler):

    @ensure_permissions("movie:read")
    def get(self):
        logging.debug("MovieListHandler. GET. auth: {}".format(self.request.headers.get("Authorization")))
        movies = db.GqlQuery(
            "SELECT * FROM Movie ORDER BY add_timestamp DESC"
        )
        movie_list = [movie.to_dict() for movie in movies]
        json_response(self, data=movie_list, status=200)

    @ensure_permissions("movie:create")
    def post(self):
        logging.debug("MovieListHandler. POST. auth: {}".format(self.request.headers.get("Authorization")))
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
        logging.debug("MovieListHandler. GET. movie_id: {}. auth: {}".format(movie_id, self.request.headers.get("Authorization")))

        ok, movie = self._get_movie(movie_id)
        if not ok:
            return

        json_response(self, movie.to_dict(), status=200)

    @ensure_permissions("movie:update")
    def post(self, movie_id):
        logging.debug(
            "MovieListHandler. POST. movie_id: {}. auth: {}".format(movie_id, self.request.headers.get("Authorization")))

        ok, movie = self._get_movie(movie_id)
        if not ok:
            return

        name = self.request.get("name", movie.name)
        description = self.request.get("description", movie.description)

        if not (name and description):
            json_response(self, {"message": "Name and description fields must be filled"}, status=400)
            return

        movie.name = name
        movie.description = description
        movie.put()
        json_response(self, status=204)

    @ensure_permissions("movie:delete")
    def delete(self, movie_id):
        logging.debug(
            "MovieListHandler. DELETE. movie_id: {}. auth: {}".format(movie_id, self.request.headers.get("Authorization")))

        ok, movie = self._get_movie(movie_id)
        if not ok:
            return

        movie.delete()
        self.response.status = 204

    def _get_movie(self, movie_id):
        """
        Get movie from datastore by movie_id
        Return status (found/not found) and movie instance
        :param movie_id: str
        """
        # movie_id is always int (based on handler regexp), but dispatcher sends as str
        movie = Movie.get_by_id(int(movie_id))
        if not movie:
            logging.debug("Movie not found. movie_id: {}. auth: {}".format(
                movie_id, self.request.headers.get("Authorization"))
            )
            json_response(self, {"message": "No such movie"}, status=404)
            return False, None
        return True, movie

