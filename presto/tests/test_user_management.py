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

        self.assertIn('Login musi mieć min 5 znaków i max 128'.encode(
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

    def test_dupliacate_user(self):
        users_count_before_post = len(User.query.all())
        user = User.query.first()

        response = self.client.post(
            '/admin/users/add',
            data=dict(login=user.login, mail=user.mail, password="admin123123"),
            follow_redirects=True
        )

        users_count_after_post = len(User.query.all())

        self.assertIn('Login lub mail jest już używany'.encode(
            encoding='utf_8'), response.get_data())

        self.assertEqual(users_count_after_post, users_count_before_post)

    def test_delete_existing_user(self):
        user_count_before_delete = User.query.count()

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

    def test_edit_user_page_exist(self):
        user = User.query.first()
        user_id = str(user.id)

        response = self.client.get('/admin/users/edit/' + user_id)

        self.assertStatus(response, 200)

    def test_edit_user(self):
        user = User.query.first()
        user_id = user.id

        response = self.client.post(
            '/admin/users/edit/' + str(user_id),
            data=dict(login="admin123452345345",mail="mail123123@mail.pl"),
            follow_redirects=True
        )

        user = User.query.filter_by(id=user_id).first()

        self.assertEqual(user.login, 'admin123452345345')
        self.assertEqual(user.mail, 'mail123123@mail.pl')

    def test_edit_user_with_invalid_data(self):
        user = User.query.first()
        user_id = user.id

        response = self.client.post(
            '/admin/users/edit/' + str(user_id),
            data=dict(login="ad",mail="mail123123"),
            follow_redirects=True
        )

        self.assertIn('Login musi mieć min 5 znaków i max 128'.encode(
            encoding='utf_8'), response.get_data())
        self.assertIn(b'Niepoprawny format email', response.get_data())

    def test_edit_user_without_data(self):
        user = User.query.first()
        user_id = user.id

        response = self.client.post(
            '/admin/users/edit/' + str(user_id),
            data=dict(),
            follow_redirects=True
        )

        self.assertIn('Pole login jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())

        self.assertIn('Pole mail jest polem wymaganym'.encode(
            encoding='utf_8'), response.get_data())


    def test_edit_to_dupliacate_user(self):
        users = User.query.all()

        user1 = users[0]
        user2 = users[1]

        response = self.client.post(
            '/admin/users/edit/' + str(user1.id),
            data=dict(login=user2.login, mail=user2.mail, password="admin123123"),
            follow_redirects=True
        )

        self.assertIn('Login lub mail jest już używany'.encode(
            encoding='utf_8'), response.get_data())

if __name__ == '__main__':
    unittest.main()
