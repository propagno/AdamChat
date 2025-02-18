import unittest
from Backend.app import app


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_register(self):
        response = self.app.post(
            '/register', json={"email": "test@example.com", "password": "password123"})
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.app.post(
            '/login', json={"email": "test@example.com", "password": "password123"})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
