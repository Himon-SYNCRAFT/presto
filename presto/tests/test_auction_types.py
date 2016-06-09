from presto.models import AuctionType
from presto.tests.base import BaseTestCase


class TestAuctionTypesTestCase(BaseTestCase):

    def test_manage_auction_types_page_exist(self):
        response = self.client.get('/admin/auction/types')

        self.assertIn(b'auction-types-list', response.data)
        self.assertIn(b'id="add-auction-type"', response.data)
        self.assertIn(b'href="/admin/auction/types/edit', response.data)
        self.assertIn(b'href="/admin/auction/types/delete', response.data)

    def test_add_auction_type(self):
        pass

    def test_add_auction_type_invalid_data(self):
        pass

    def test_add_auction_type_duplicate(self):
        pass

    def test_edit_auction_type(self):
        pass

    def test_edit_auction_type_invalid_data(self):
        pass

    def test_edit_auction_type_duplicate(self):
        pass

    def test_delete_auction_type(self):
        pass

    def test_delete_not_existing_auction_type(self):
        pass
