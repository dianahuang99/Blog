"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    

class User(db.Model):
    """User"""

    __tablename__ = "User"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text,
                     nullable=False)
    image_url = db.Column(db.Text, nullable=False, default="https://thevoicefinder.com/wp-content/themes/the-voice-finder/images/default-img.png")
