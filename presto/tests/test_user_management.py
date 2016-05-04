import unittest
from presto import app


class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_can_show_users(self):
        response = self.client.get('/manage_users')

        assert 'users-table' in response.data


if __name__ == '__main__':
    unittest.main()
