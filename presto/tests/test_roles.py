from presto.tests.base import BaseTestCase
from presto.models import Role, User
from presto.database import db_session
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

        response = self.client.post('/admin/users/roles/add',
                                    data={'name': new_name},
                                    follow_redirects=True)

        count_after_post = Role.query.count()

        self.assertEqual(count_before_post, count_after_post)

        self.assertIsNone(Role.query.filter_by(name=new_name).first())
        self.assertIn('Nazwa musi mieć max 128 znaków'.encode(
            encoding='utf_8'), response.get_data())

        new_name = ""

        response = self.client.post('/admin/users/roles/add',
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

        response = self.client.post('/admin/users/roles/add',
                                    data={'name': new_name},
                                    follow_redirects=True)

        count_after_post = Role.query.count()

        self.assertEqual(count_before_post, count_after_post)
        self.assertIn('Nazwa jest już zajęta'.encode(
            encoding='utf_8'), response.get_data())

    def test_edit_role(self):
        role = Role.query.first()
        role_id = str(role.id)

        name = 'super admin'

        count_before_post = Role.query.count()

        response = self.client.post('/admin/users/roles/edit/' + role_id,
                                    data=dict(name=name), follow_redirects=True)

        count_after_post = Role.query.count()
        role = Role.query.filter_by(id=role.id).first()

        self.assertEqual(count_before_post, count_after_post)
        self.assertStatus(response, 200)
        self.assertEqual(role.name, name)

    def test_edit_role_invalid_data(self):
        role = Role.query.first()
        role_id = str(role.id)
        old_name = role.name

        name = "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334"

        count_before_post = Role.query.count()

        response = self.client.post('/admin/users/roles/edit/' + role_id,
                                    data=dict(name=name), follow_redirects=True)

        count_after_post = Role.query.count()
        role = Role.query.filter_by(id=role.id).first()

        self.assertEqual(count_before_post, count_after_post)
        self.assertStatus(response, 200)
        self.assertEqual(role.name, old_name)
        self.assertIn('Nazwa musi mieć max 128 znaków'.encode(
            encoding='utf_8'), response.get_data())

        name = ""

        response = self.client.post('/admin/users/roles/add',
                                    data=dict(name=name),
                                    follow_redirects=True)

        count_after_post = Role.query.count()

        self.assertEqual(count_before_post, count_after_post)
        self.assertStatus(response, 200)
        self.assertIn('Pole nazwa jest wymagane'.encode(
            encoding='utf_8'), response.get_data())

    def test_edit_role_duplicate(self):
        role = Role.query.first()
        role_id = str(role.id)
        old_name = role.name
        name = 'client'

        response = self.client.post('/admin/users/roles/edit/' + role_id,
                                    data=dict(name=name), follow_redirects=True)

        self.assertStatus(response, 200)
        self.assertIn('Nazwa jest już zajęta'.encode(
            encoding='utf_8'), response.get_data())
        self.assertEqual(role.name, old_name)

    def test_edit_not_existing_role(self):
        response = self.client.post('/admin/users/roles/edit/' + 'asd',
                                    data=dict(name='asd'), follow_redirects=True)

        self.assertStatus(response, 404)

    def test_delete_role(self):
        new_role = Role(name='super_admin')
        db_session.add(new_role)
        db_session.commit()

        role = Role.query.filter_by(name='super_admin').first()
        role_id = str(role.id)

        count_before_delete = Role.query.count()
        response = self.client.get('/admin/users/roles/delete/' + role_id)
        count_after_delete = Role.query.count()

        self.assertStatus(response, 302)
        self.assertIsNone(Role.query.filter_by(id=role.id).first())
        self.assertEqual(count_before_delete, count_after_delete + 1)

    def test_delete_used_role(self):
        user = User.query.first()
        role = Role.query.filter_by(id=user.role_id).first()
        role_id = str(role.id)

        count_before_delete = Role.query.count()
        response = self.client.get('/admin/users/roles/delete/' + role_id)
        count_after_delete = Role.query.count()

        self.assertStatus(response, 302)
        self.assertIsNotNone(Role.query.filter_by(id=role.id).first())
        self.assertEqual(count_before_delete, count_after_delete)

    def test_delete_not_existing_role(self):
        response = self.client.get('/admin/users/roles/delete/' + 'asdasd')

        self.assertStatus(response, 404)
