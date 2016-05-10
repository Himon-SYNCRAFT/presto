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

    def test_add_new_user_with_invalid_data(self):
        response = self.client.post(
            '/admin/users/add',
            data=dict(login="ad",
                      mail="mail123123", password="admin123123"),
            follow_redirects=True
        )

        self.assertIn('Login musi mieć min 6 znaków i max 128'.encode(
            encoding='utf_8'), response.get_data())
        self.assertIn(b'Niepoprawny format email', response.get_data())

    def test_add_new_user_without_data(self):
        response = self.client.post(
            '/admin/users/add',
            data=dict(login="",
                      mail="", password=""),
            follow_redirects=True
        )

        self.assertIn('Pole login jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())
        self.assertIn('Pole mail jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())
        self.assertIn('Pole hasło jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())

    def test_delete_user(self):
        pass

    def test_edit_user(self):
        pass


if __name__ == '__main__':
    unittest.main()
