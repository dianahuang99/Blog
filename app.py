"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.sql import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def show_home():
    """Redirect to list of users."""
    return redirect("/users")


@app.route("/users")
def show_users():
    """Show all users."""
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/new")
def show_user_form():
    """Show an add form for users."""

    return render_template("new_user_form.html")


@app.route("/users/new", methods=["POST"])
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if image_url == "":
        new_user = User(first_name=f"{first_name}", last_name=f"{last_name}")
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    new_user = User(
        first_name=f"{first_name}", last_name=f"{last_name}", image_url=f"{image_url}"
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Show information about the given user."""
    user = User.query.get(user_id)
    return render_template("user_info.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_user(user_id):
    """Show the edit page for a user."""
    user = User.query.get(user_id)
    return render_template("edit_user_form.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def process_edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if first_name != "":
        user = User.query.get(f"{user_id}")
        user.first_name = first_name
        db.session.commit()
    if last_name != "":
        user = User.query.get(f"{user_id}")
        user.last_name = last_name
        db.session.commit()
    if image_url != "":
        user = User.query.get(f"{user_id}")
        user.image_url = image_url
        db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    user = User.query.filter_by(id=f"{user_id}").first()
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show the post form."""
    user = User.query.get(user_id)
    return render_template("new_post_form.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Process the add form, adding a new post and going back to /users"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user,
        tags=tags,
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post_info(post_id):
    """Show the posts."""
    post = Post.query.get(post_id)
    return render_template("post_info.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    """Show the edit page for a post."""
    post = Post.query.get(post_id)
    return render_template("edit_post_form.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Process the edit form, returning the user to the /post info page."""
    post = Post.query.get(post_id)

    title = request.form["title"]
    content = request.form["content"]

    if title != "":
        post.title = title
        db.session.commit()
    if content != "":
        post.content = content
        db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Process the deletion, returning the user to the user info page."""
    post = Post.query.get(post_id)
    user = User.query.get(post.user_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user.id}")


@app.route("/tags")
def show_tags():
    """Show all tags."""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_post(tag_id):
    """Show posts with given tag."""
    tag = Tag.query.get(tag_id)
    return render_template("show_posts.html", tag=tag)


@app.route("/tags/new")
def show_tag_form():
    """Show an add form for tags."""

    return render_template("new_tag_form.html")


@app.route("/tags/new", methods=["POST"])
def add_new_tag():
    """Process the add form, adding a new tag and going back to /tags"""
    name = request.form["name"]

    new_tag = Tag(name=f"{name}")
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag(tag_id):
    """Show the edit page for a tag."""
    tag = Tag.query.get(tag_id)
    return render_template("edit_tag_form.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Process the edit form, returning the user to the /tags/1 info page."""
    tag = Tag.query.get(tag_id)

    name = request.form["name"]

    if name != "":
        tag.name = name
        db.session.commit()
    return redirect(f"/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag and return to /tags page."""
    Tag.query.filter_by(id=f"{tag_id}").delete()
    db.session.commit()
    return redirect("/tags")


@app.route("/posts/<int:post_id>/edit/tags")
def show_add_tags(post_id):
    """Show the tags."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("add_tags.html", tags=tags, post=post)


@app.route("/posts/<int:post_id>/edit/tags", methods=["POST"])
def set_tags(post_id):
    """Set the tags."""
    post = Post.query.get_or_404(post_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("/users/<int:user_id>/posts/new/tags")
def show_tags_new_post(user_id):
    """Show the tags."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_tags.html", tags=tags, user=user)


@app.route("/users/<int:user_id>/posts/new/tags", methods=["POST"])
def set_tags_new_post(user_id):
    """Show the tags."""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
        title=request.form["title"],
        content=request.form["content"],
        user=user,
        tags=tags,
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/posts/{{new_post.id}}/edit/tags")
