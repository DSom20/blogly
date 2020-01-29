"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect('/users')


@app.route('/users')
def show_users():

    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def show_create_user_form():
    return render_template('users_new.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url or None

    user = User(first_name=first_name, last_name=last_name, 
                image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


