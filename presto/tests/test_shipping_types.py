import unittest

from presto.database import db_session
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
        shipping_types = ShippingType.query.all()
        count_shipping_types_before_post = ShippingType.query.count()

        self.client.post('/admin/shipping/types/add',
                         data={'name': 'Paczkomat123'},
                         follow_redirects=True)

        ShippingType.query.filter_by(
            name='Paczkomat123', is_boolean=False).one()

        self.client.post('/admin/shipping/types/add',
                         data={'name': 'Paczkomat123'},
                         follow_redirects=True)

        ShippingType.query.filter_by(
            name='Paczkomat123', is_boolean=False).one()

        count_shipping_types_after_post = ShippingType.query.count()

        self.assertEqual(count_shipping_types_before_post + 1,
                         count_shipping_types_after_post)
