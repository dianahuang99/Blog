from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class PetViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample User."""

        User.query.delete()

        user = User(first_name="Diana", last_name="Huang", image_url="https://w7.pngwing.com/pngs/264/154/png-transparent-chibi-anime-mangaka-drawing-kawaii-chibi-thumbnail.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.image_url = user.image_url

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        
    def test_redirection(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")
    
    def test_redirection_followed(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{self.first_name}", html)
            
    def test_show_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_add_new_user(self):
        with app.test_client() as client:
            d = {'first_name':f"{self.first_name}", 'last_name':f"{self.last_name}", "image_url":f"{self.image_url}"}
            resp = client.post('/users/new',
                                data=d)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")
            
    def test_redirection_followed_after_user_add(self):
        with app.test_client() as client:
            d = {'first_name':f"{self.first_name}", 'last_name':f"{self.last_name}", "image_url":f"{self.image_url}"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            
    def test_default_image_after_user_add(self):
        with app.test_client() as client:
            d = {'first_name':f"{self.first_name}", 'last_name':f"{self.last_name}", "image_url":""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.image_url, "https://w7.pngwing.com/pngs/264/154/png-transparent-chibi-anime-mangaka-drawing-kawaii-chibi-thumbnail.png")
            
    def test_show_user_info(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>{self.first_name} {self.last_name}</h1>", html)

    def test_show_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'name="first_name" value="{self.first_name}"', html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            d = {'first_name':"New Name", 'last_name':f"{self.last_name}", "image_url":f"{self.image_url}"}
            resp = client.post(f'/users/{self.user_id}/edit', data=d)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")
            
    def test_redirection_followed_after_edit_user(self):
        with app.test_client() as client:
            d = {'first_name':"New Name", 'last_name':f"{self.last_name}", "image_url":f"{self.image_url}"}
            resp = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/users/{self.user_id}">New Name {self.last_name}</a>', html)
    
    def test_delete_user(self):
        with app.test_client() as client:
            d = {'first_name':f"{self.first_name}", 'last_name':f"{self.last_name}", "image_url":f"{self.image_url}"}
            resp = client.post(f'/users/{self.user_id}/delete',data=d)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")
    
    def test_redirection_followed_after_delete(self):
        with app.test_client() as client:
            d = {'first_name':f"{self.first_name}", 'last_name':f"{self.last_name}", "image_url":f"{self.image_url}"}
            resp = client.post(f'/users/{self.user_id}/delete', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f'<a href="/users/{self.user_id}">{self.first_name} {self.last_name}</a>', html)