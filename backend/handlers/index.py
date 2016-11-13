import os

import webapp2


from backend.settings import TEMPLATES_DIR


class IndexHandler(webapp2.RequestHandler):

    def get(self):
        from google.appengine.ext.webapp import template
        movie_template_path = os.path.join(TEMPLATES_DIR, "index.html")
        self.response.write(template.render(movie_template_path, {}))
