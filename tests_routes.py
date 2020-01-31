from app import app
from models import db, connect_db, User, Post
from unittest import TestCase
from global_variables import DEFAULT_IMAGE_URL

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

connect_db(app)
db.drop_all()
db.create_all()
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTesting(TestCase):
    """ Route Testing """

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        db.create_all()
        user1 = User(first_name='David', last_name='Sommers')
        post1 = Post(title='Test Post', content='Content for tester post :)', user_id=1)
        db.session.add(user1)
        db.session.add(post1)
        db.session.commit()

    def tearDown(self):
        """Stuff to do after every test"""

        # Need to drop_all vs just delete, since just deleting doesn't reset
        #   the primary key autoincrementor, and our tests depend on hardcoding
        #   the user.id of '1' into the urls frequently
        # User.query.delete()
        db.drop_all()

    def test_root_redirection_followed(self):
        with self.client as client:
            resp = client.get('/', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_users(self):
        with self.client as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertIn('David', html)

    def test_users_details(self):
        with self.client as client:
            resp = client.get('/users/1')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>David Sommers</h1>', html)
            self.assertIn(f'<img src={DEFAULT_IMAGE_URL}',
                          html)

    def test_users_edit(self):
        # Get Request
        with self.client as client:
            resp = client.get('/users/1/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit a user</h1>', html)

            self.assertIn('<input id="first_name" type="text" name="first_name" value=David',
                          html)
            self.assertIn('<input id="last_name" type="text" name="last_name" value=Sommers',
                          html)
            self.assertNotIn(f'value={DEFAULT_IMAGE_URL}',
                             html)

        # Post Request
        with self.client as client:
            resp = client.post('/users/1/edit', data=dict(first_name='David',
                               last_name='Truman', image_url=''),
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            user_1 = User.query.get(1)

            self.assertEqual(User.query.count(), 1)
            self.assertEqual(user_1.first_name, 'David')
            self.assertEqual(user_1.last_name, 'Truman')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

            self.assertIn('<li><a href=/users/1>David Truman</a></li>', html)

    def test_users_new(self):
        # Get request
        with self.client as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_users_post(self):
        # Post request
        with self.client as client:
            resp = client.post('users/new', data=dict(first_name='Bob',
                               last_name='Johnson', image_url=''),
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            user_2 = User.query.get(2)

            self.assertEqual(User.query.count(), 2)
            self.assertEqual(user_2.first_name, 'Bob')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

            self.assertIn('<li><a href=/users/2>Bob Johnson</a></li>', html)

    def test_users_delete(self):
        with self.client as client:
            resp = client.post('/users/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(User.query.count(), 0)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

            self.assertNotIn('David', html)

    
    def test_posts_new(self):
        # Get request
        with self.client as client:
            resp = client.get('/users/1/posts/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add Post for David Sommers</h1>', html)
    
    def test_posts(self):
        # Post request
        with self.client as client:
            resp = client.post('/users/1/posts/new', data=dict(title='Another Test Post',
                               content="Content for another test post."),
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            post_2 = Post.query.get(2)

            self.assertEqual(Post.query.count(), 2)
            self.assertEqual(post_2.user.full_name, 'David Sommers')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>David Sommers</h1>', html)

            self.assertIn('<li><a href=/posts/2>Another Test Post</a></li>', html)

    def test_bad_id(self):
        with self.client as client:
            resp = client.post('/user/123123/posts/new')

            self.assertEqual(resp.status_code, 404)

    def test_users_delete(self):
        with self.client as client:
            resp = client.post('/posts/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(Post.query.count(), 0)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>David Sommers</h1>', html)

            self.assertNotIn('Test', html)