import webapp2
from backend.routes import routes


app = webapp2.WSGIApplication(routes=routes, debug=True)
