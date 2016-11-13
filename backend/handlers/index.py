import os

import webapp2
from google.appengine.ext.webapp import template

from settings import TEMPLATES_DIR


class IndexHandler(webapp2.RequestHandler):

    def get(self):
        movie_template_path = os.path.join(TEMPLATES_DIR, "index.html")
        self.response.write(template.render(movie_template_path, {}))
