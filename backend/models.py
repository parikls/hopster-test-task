from google.appengine.ext import db


class User(db.Model):

    email = db.EmailProperty(required=True)
    password = db.StringProperty(required=True)
    registration_timestamp = db.DateTimeProperty(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.key().id(),
            "name": self.email,
            "registration_timestamp": self.registration_timestamp.strftime("%d.%m.%y %H:%M")
        }


class Movie(db.Model):

    name = db.StringProperty(required=True)
    description = db.TextProperty(required=True)
    add_timestamp = db.DateTimeProperty(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.key().id(),
            "name": self.name,
            "description": self.description,
            "add_timestamp": self.add_timestamp.strftime("%d.%m.%y %H:%M")
        }