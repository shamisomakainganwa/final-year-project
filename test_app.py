import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_login_valid(self):
        # Test valid login credentials
        response = self.app.post('/login', data={'username': 'user1', 'password': 'password1'})
        self.assertEqual(response.status_code, 302)  # Check if redirected to index page

    def test_login_invalid(self):
        # Test invalid login credentials
        response = self.app.post('/login', data={'username': 'invalid_user', 'password': 'invalid_password'})
        self.assertIn(b'Invalid username or password', response.data)  # Check for error message

    def test_predict(self):
        # Test chatbot prediction endpoint
        response = self.app.post('/null/predict', json={'message': 'Hello'})
        self.assertEqual(response.status_code, 200)  # Check if response status is OK

if __name__ == '__main__':
    unittest.main()
