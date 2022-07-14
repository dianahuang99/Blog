"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
    """Redirect to list of users."""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Show all users."""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_user_form():
    """Show an add form for users."""
    
    return render_template('new_user_form.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    if image_url == "":
        new_user = User(first_name=f"{first_name}", last_name=f"{last_name}")
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')
    new_user = User(first_name=f"{first_name}", last_name=f"{last_name}", image_url=f"{image_url}")
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show information about the given user."""
    user = User.query.get(user_id)
    return render_template('user_info.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Show the edit page for a user."""
    user = User.query.get(user_id)
    return render_template('edit_user_form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
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
    return redirect('/users')
    

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    User.query.filter_by(id=f"{user_id}").delete()
    db.session.commit()
    return redirect('/users')