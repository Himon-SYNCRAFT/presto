from presto.models import ShippingType
from presto.tests.base import BaseTestCase


class TestShippingTypesTestCase(BaseTestCase):

    def test_shipping_types_manage_page_exist(self):
        response = self.client.get('/admin/shipping/types')
        self.assertIn(b'shipping-types-list', response.data)
        self.assertIn(b'id="add-shipping-type"', response.data)
        self.assertIn(b'href="/admin/shipping/types/edit', response.data)
        self.assertIn(b'href="/admin/shipping/types/delete', response.data)

    def test_add_shipping_type_proper_data(self):
        count_shipping_types_before_post = ShippingType.query.count()

        self.client.post('/admin/shipping/types/add',
                         data={'name': 'Paczkomat123'},
                         follow_redirects=True)

        count_shipping_types_after_post = ShippingType.query.count()

        self.assertEqual(count_shipping_types_before_post + 1,
                         count_shipping_types_after_post)

        ShippingType.query.filter_by(
            name='Paczkomat123', is_boolean=False).one()

    def test_add_shipping_type_invalid_data(self):
        count_shipping_types_before_post = ShippingType.query.count()

        self.client.post('/admin/shipping/types/add',
                         data={'name': None,
                               'is_boolean': None},
                         follow_redirects=True)

        count_shipping_types_after_post = ShippingType.query.count()

        self.assertEqual(count_shipping_types_before_post,
                         count_shipping_types_after_post)

    def test_add_duplicate_shipping_type(self):
        count_shipping_types_before_post = ShippingType.query.count()

        self.client.post('/admin/shipping/types/add',
                         data={'name': 'Paczkomat123'},
                         follow_redirects=True)

        ShippingType.query.filter_by(
            name='Paczkomat123', is_boolean=False).one()

        response = self.client.post('/admin/shipping/types/add',
                                    data={'name': 'Paczkomat123'},
                                    follow_redirects=True)

        ShippingType.query.filter_by(
            name='Paczkomat123', is_boolean=False).one()

        count_shipping_types_after_post = ShippingType.query.count()

        self.assertEqual(count_shipping_types_before_post + 1,
                         count_shipping_types_after_post)

        self.assertIn('Nazwa jest już zajęta'.encode(
            encoding='utf_8'), response.get_data())

    def test_edit_shipping_types(self):
        item = ShippingType.query.first()

        new_name = item.name + '1234'
        new_is_boolen = True

        self.client.post(
            '/admin/shipping/types/edit/' + str(item.id),
            data={'name': new_name, 'is_boolean': new_is_boolen}
        )

        item = ShippingType.query.filter_by(id=item.id).first()

        self.assertEqual(item.name, new_name)
        self.assertEqual(item.is_boolean, new_is_boolen)

    def test_edit_shipping_types_invalid_data(self):
        item = ShippingType.query.first()
        count_shipping_types_before_post = ShippingType.query.count()

        response = self.client.post(
            '/admin/shipping/types/edit/' + str(item.id),
            data={'name': None, 'is_boolean': None},
        )

        count_shipping_types_after_post = ShippingType.query.count()

        self.assertEqual(
            count_shipping_types_before_post, count_shipping_types_after_post)

        self.assertIn('Pole nazwa jest wymagane'.encode(
            encoding='utf_8'), response.get_data())

    def test_edit_shipping_types_duplicate(self):
        item = ShippingType.query.filter_by(id=2).first()
        count_shipping_types_before_post = ShippingType.query.count()

        response = self.client.post('/admin/shipping/types/edit/1',
                                    data={'name': item.name},
                                    follow_redirects=True)

        count_shipping_types_after_post = ShippingType.query.count()

        self.assertEqual(count_shipping_types_before_post,
                         count_shipping_types_after_post)

        self.assertIn('Nazwa jest już zajęta'.encode(
            encoding='utf_8'), response.get_data())

    def test_edit_shipping_types_not_exist(self):
        response = self.client.get('/admin/shipping/types/edit/1234')

        self.assertStatus(response, 404)

        response = self.client.post('/admin/shipping/types/edit/1234',
                                    data={'name': 'Paczkomat123'},
                                    follow_redirects=True)

        self.assertStatus(response, 404)

    def test_delete_shipping_type(self):
        item = ShippingType.query.first()
        count_shipping_types_before_post = ShippingType.query.count()

        self.client.get('/admin/shipping/types/delete/' + str(item.id))

        count_shipping_types_after_post = ShippingType.query.count()

        self.assertEqual(count_shipping_types_before_post,
                         count_shipping_types_after_post + 1)

        self.assertIsNone(ShippingType.query.filter_by(id=item.id).first())

    def test_delete_not_existing_shipping_type(self):
        response = self.client.get('/admin/shipping/types/delete/1234')

        self.assertStatus(response, 404)
