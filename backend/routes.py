import webapp2

from handlers.api.auth import LoginHandler
from handlers.api.movie import MovieListHandler, MovieDetailsHandler
from handlers.index import IndexHandler

routes = [

    # API routes
    webapp2.Route(r'/api/movie/', handler=MovieListHandler, name='movie_api_list'),
    webapp2.Route(r'/api/movie/<movie_id:\d+>/', handler=MovieDetailsHandler, name='movie_api_details'),
    webapp2.Route(r'/api/auth/login/', handler=LoginHandler, name='auth_api_login'),

    # template routes
    webapp2.Route(r'/', handler=IndexHandler, name='movie_template_handler'),
]
