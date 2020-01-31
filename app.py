"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension
from global_variables import DEFAULT_IMAGE_URL

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
    [first_name, last_name, image_url] = [request.form['first_name'], 
                                          request.form['last_name'],
                                          request.form['image_url'] or None]

    user = User(first_name=first_name, last_name=last_name, 
                image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>')
def show_user(user_id):
    user = User.query.get(user_id)
    return render_template('user_details.html', user=user)


@app.route('/users/<user_id>/edit')
def show_edit_user(user_id):
    user = User.query.get(user_id)
    return render_template('user_edit.html', user=user)


@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    [user.first_name, user.last_name, user.image_url] = [request.form['first_name'], 
                                                         request.form['last_name'],
                                                         request.form['image_url'] or None]
    if user.image_url is None:
        user.image_url = DEFAULT_IMAGE_URL
    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<user_id>/posts/new')
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('/post_new.html', user=user, tags=tags)


@app.route('/users/<user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    for tag_name in request.form:
        if request.form[tag_name] == 'on':
            print(f'**************************{tag_name}')
            tag = Tag.query.filter_by(name=tag_name).first()
            print(tag)
            post_tag = PostTag(post_id=post.id, tag_id=tag.id)
            db.session.add(post_tag)
    
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('posts.html', post=post)


@app.route('/posts/<post_id>/edit')
def show_edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    tags = Tag.query.all()

    return render_template('post_edit.html', post=post, tags=tags)


@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    print(request.form)
    for tag_name in request.form:
        if request.form[tag_name] == 'on':
            tag = Tag.query.filter_by(name=tag_name).first()
            post_tag = PostTag.query.filter_by(post_id=post.id, tag_id=tag.id).first() or PostTag(post_id=post.id, tag_id=tag.id)
            db.session.add(post_tag)
    
    

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_home = post.user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_home}')


@app.route('/tags')
def show_all_tags():
    tags = Tag.query.all()
    return render_template('show_tags.html', tags=tags)


@app.route('/tags/<tag_id>')
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)


@app.route('/tags/new')
def new_tag():
    return render_template('create_tag.html')


@app.route('/tags/new', methods=['POST'])
def create_new_tag():
    name = request.form["name"]
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<tag_id>/edit')
def show_edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    name = request.form["name"]
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    
    return redirect("/tags")


@app.route('/tags/<tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
    