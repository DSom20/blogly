"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"


def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User. """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    image_url = db.Column(db.String,
                          nullable=True, default=DEFAULT_IMAGE_URL)

    def update_user(self, first_name, last_name, image_url):
        """ Update all 3 attributes of a user """

        self.first_name = first_name
        self.last_name = last_name
        self.image_url = DEFAULT_IMAGE_URL if image_url is None else image_url
