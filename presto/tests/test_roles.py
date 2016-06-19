from presto.tests.base import BaseTestCase
from presto.models import Role
from unittest import skip


class TestRolesManagement(BaseTestCase):

    def test_role_page_exist(self):
        response = self.client.get('/admin/users/roles')

        self.assertStatus(response, 200)
        self.assertIn(b'id="roles-list"', response.data)

    def test_add_new_role(self):
        count_before_post = len(Role.query.all())
        role_name = 'super admin'

        response = self.client.post(
            '/admin/users/roles/add',
            data=dict(name=role_name),
            follow_redirects=True
        )

        self.assertStatus(response, 200)

        count_after_post = len(Role.query.all())

        role = Role.query.filter_by(name=role_name).first()

        self.assertIsNotNone(role)
        self.assertEqual(count_before_post + 1, count_after_post)
        self.assertIn(role.name.encode(encoding='utf-8'), response.get_data())

    def test_add_new_role_invalid_data(self):
        count_before_post = Role.query.count()
        new_name = "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334"

        response = self.client.post('/admin/auction/types/add',
                                    data={'name': new_name},
                                    follow_redirects=True)

        count_after_post = Role.query.count()

        self.assertEqual(count_before_post, count_after_post)

        self.assertIsNone(Role.query.filter_by(name=new_name).first())
        self.assertIn('Nazwa musi mieć max 128 znaków'.encode(
            encoding='utf_8'), response.get_data())

        new_name = ""

        response = self.client.post('/admin/auction/types/add',
                                    data={'name': new_name},
                                    follow_redirects=True)

        count_after_post = Role.query.count()

        self.assertEqual(count_before_post, count_after_post)

        self.assertIn('Pole nazwa jest wymagane'.encode(
            encoding='utf_8'), response.get_data())

    def test_add_duplicate_role(self):
        count_before_post = Role.query.count()
        new_name = 'admin'

        self.assertIsNotNone(Role.query.filter_by(name=new_name).first())

        response = self.client.post('/admin/auction/types/add',
                                    data={'name': 'zwykła'},
                                    follow_redirects=True)

        count_after_post = Role.query.count()

        self.assertEqual(count_before_post, count_after_post)
        self.assertIn('Nazwa jest już zajęta'.encode(
            encoding='utf_8'), response.get_data())
