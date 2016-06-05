import unittest

from presto.models import ShippingType
from presto.tests.base import BaseTestCase

class TestShippingTypesTestCase(BaseTestCase):

    def test_shipping_types_manage_page_exist(self):
        response = self.client.get('/admin/shipping/types')
        self.assertIn(b'shipping-types-list', response.data)
        self.assertIn(b'id="add-shipping-type"', response.data)
        self.assertIn(b'href="/admin/shipping/types/edit', response.data)
        self.assertIn(b'href="/admin/shipping/types/delete', response.data)
