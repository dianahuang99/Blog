"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(
        db.Text,
        nullable=False,
        default="https://thevoicefinder.com/wp-content/themes/the-voice-finder/images/default-img.png",
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class Post(db.Model):
    """Post"""

    __tablename__ = "Post"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    # user = db.relationship("User", backref="posts")

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    tags = db.relationship(
        "Tag", secondary="PostTag", cascade="all,delete", backref="posts"
    )


class Tag(db.Model):
    """Tag"""

    __tablename__ = "Tag"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    # posts = db.relationship(
    #     "Post",
    #     secondary="PostTag",
    #     cascade="all,delete",
    #     backref="tags",
    # )


class PostTag(db.Model):
    """PostTag"""

    __tablename__ = "PostTag"

    post_id = db.Column(db.Integer, db.ForeignKey("Post.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("Tag.id"), primary_key=True)
