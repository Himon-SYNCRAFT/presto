import unittest
from presto import app
from presto.tests.base import BaseTestCase


class TestUserManagement(BaseTestCase):

    def test_manage_users_view_show_users(self):
        response = self.client.get('/admin/users')

        self.assertIn(b'id="users-list"', response.data)

    def test_add_new_user_proper_data(self):
        response = self.client.post(
            '/admin/users/add',
            data=dict(login="admin123452345345",
                      mail="mail123123@mail.pl", password="admin123123"),
            follow_redirects=True
        )

        self.assertIn(b'id="users-list"', response.get_data())


if __name__ == '__main__':
    unittest.main()
