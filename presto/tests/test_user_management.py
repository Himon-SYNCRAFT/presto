import unittest

from presto import app
from presto.models import User
from presto.tests.base import BaseTestCase


class TestUserManagement(BaseTestCase):

    def test_manage_users_view_show_users(self):
        response = self.client.get('/admin/users')

        self.assertIn(b'id="users-list"', response.data)

    def test_add_new_user_proper_data(self):
        users_count_before_post = len(User.query.all())

        response = self.client.post(
            '/admin/users/add',
            data=dict(login="admin123452345345",
                      mail="mail123123@mail.pl", password="admin123123"),
            follow_redirects=True
        )

        users_count_after_post = len(User.query.all())

        self.assertIn(b'id="users-list"', response.get_data())
        self.assertEqual(users_count_after_post, users_count_before_post + 1)

    def test_add_new_user_with_invalid_data(self):
        users_count_before_post = len(User.query.all())

        response = self.client.post(
            '/admin/users/add',
            data=dict(login="ad",
                      mail="mail123123", password="admin123123"),
            follow_redirects=True
        )

        users_count_after_post = len(User.query.all())

        self.assertIn('Login musi mieć min 6 znaków i max 128'.encode(
            encoding='utf_8'), response.get_data())
        self.assertIn(b'Niepoprawny format email', response.get_data())
        self.assertEqual(users_count_after_post, users_count_before_post)

    def test_add_new_user_without_data(self):
        users_count_before_post = len(User.query.all())

        response = self.client.post(
            '/admin/users/add',
            data=dict(login="",
                      mail="", password=""),
            follow_redirects=True
        )

        users_count_after_post = len(User.query.all())

        self.assertIn('Pole login jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())

        self.assertIn('Pole mail jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())

        self.assertIn('Pole hasło jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())

        self.assertEqual(users_count_after_post, users_count_before_post)

    def test_add_new_user_with_invalid_mail_format(self):
        users_count_before_post = len(User.query.all())

        response = self.client.post(
            '/admin/users/add',
            data=dict(login="admin123452345345",
                      mail="mail123123", password="admin123123"),
            follow_redirects=True
        )

        users_count_after_post = len(User.query.all())

        self.assertIn('Niepoprawny format email'.encode(
            encoding='utf_8'), response.get_data())

        self.assertEqual(users_count_after_post, users_count_before_post)

    def test_delete_existing_user(self):
        user_count_before_delete = User.query.count()

        if user_count_before_delete == 0:
            return

        user = User.query.first()

        user_id = str(user.id)
        self.client.get('/admin/users/delete/' + user_id)

        user_count_after_delete = User.query.count()

        self.assertEqual(user_count_before_delete, user_count_after_delete + 1)

    def test_delete_not_existing_user(self):
        response = self.client.get('/admin/users/delete/' + '99')

        self.assertStatus(response, 404)

    def test_delete_invalid_id(self):
        response = self.client.get('/admin/users/delete/' + 'abc')

        self.assertStatus(response, 404)

    def test_edit_user(self):
        pass


if __name__ == '__main__':
    unittest.main()
