"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime
from global_variables import DEFAULT_IMAGE_URL

db = SQLAlchemy()

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
    posts = db.relationship('Post', backref='user')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Name: {self.full_name}, # of Posts: {len(self.posts)}>"

class Post(db.Model):
    """ Posts. """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Title: {self.title}, User ID: {self.user.id}>"

