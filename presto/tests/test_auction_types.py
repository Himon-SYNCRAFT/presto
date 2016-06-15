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
        count_before_post = AuctionType.query.count()

        self.client.post('/admin/auction/types/add',
                         data={'name': 'niezwykla'},
                         follow_redirects=True)

        count_after_post = AuctionType.query.count()

        self.assertEqual(count_before_post + 1, count_after_post)

        AuctionType.query.filter_by(name='niezwykla').one()

    def test_add_auction_type_invalid_data(self):
        count_before_post = AuctionType.query.count()
        new_name = "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334"

        response = self.client.post('/admin/auction/types/add',
                                    data={'name': new_name},
                                    follow_redirects=True)

        count_after_post = AuctionType.query.count()

        self.assertEqual(count_before_post, count_after_post)

        self.assertIsNone(AuctionType.query.filter_by(name=new_name).first())
        self.assertIn('Nazwa musi mieć max 128 znaków'.encode(
            encoding='utf_8'), response.get_data())

    def test_add_auction_type_duplicate(self):
        count_before_post = AuctionType.query.count()
        self.assertIsNotNone(
            AuctionType.query.filter_by(name='zwykła').first())

        response = self.client.post('/admin/auction/types/add',
                                    data={'name': 'zwykła'},
                                    follow_redirects=True)

        count_after_post = AuctionType.query.count()

        self.assertEqual(count_before_post, count_after_post)
        self.assertIn('Nazwa jest już zajęta'.encode(
            encoding='utf_8'), response.get_data())

    def test_add_auction_type_without_data(self):
        count_before_post = AuctionType.query.count()
        new_name = ""

        response = self.client.post('/admin/auction/types/add',
                                    data={'name': new_name},
                                    follow_redirects=True)

        count_after_post = AuctionType.query.count()

        self.assertEqual(count_before_post,
                         count_after_post)

        self.assertIsNone(AuctionType.query.filter_by(name=new_name).first())
        self.assertIn('Pole nazwa jest wymagane'.encode(
            encoding='utf_8'), response.get_data())

    def test_edit_auction_type(self):
        auction_type = AuctionType.query.first()
        type_name = auction_type.name
        count_before_post = AuctionType.query.count()

        response = self.client.post('/admin/auction/types/edit/' + str(auction_type.id),
                                    data={'name': 'niezwykla'},
                                    follow_redirects=True)

        self.assert_200(response)

        count_after_post = AuctionType.query.count()

        self.assertEqual(count_before_post, count_after_post)

        self.assertIsNone(AuctionType.query.filter_by(name=type_name).first())
        self.assertIsNotNone(
            AuctionType.query.filter_by(name='niezwykla').first())

    def test_edit_auction_type_invalid_data(self):
        auction_type = AuctionType.query.first()
        old_name = auction_type.name

        count_before_post = AuctionType.query.count()
        new_name = "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334" + \
            "12345678910111213141516171819202122232425262728293031323334"

        response = self.client.post('/admin/auction/types/edit/' + str(auction_type.id),
                                    data={'name': new_name},
                                    follow_redirects=True)

        count_after_post = AuctionType.query.count()

        self.assertEqual(count_before_post, count_after_post)

        self.assertIsNone(AuctionType.query.filter_by(name=new_name).first())
        self.assertIsNotNone(
            AuctionType.query.filter_by(name=old_name).first())

        self.assertIn('Nazwa musi mieć max 128 znaków'.encode(
            encoding='utf_8'), response.get_data())

    def test_edit_auction_type_duplicate(self):
        auction_types = AuctionType.query.all()
        auction_type1 = auction_types[0]
        auction_type2 = auction_types[1]

        count_before_post = AuctionType.query.count()

        self.assertIsNotNone(auction_type1)
        self.assertIsNotNone(auction_type2)

        response = self.client.post('/admin/auction/types/edit/' + str(auction_type1.id),
                                    data={'name': auction_type2.name},
                                    follow_redirects=True)

        count_after_post = AuctionType.query.count()

        self.assertEqual(count_before_post, count_after_post)
        self.assertIn('Nazwa jest już zajęta'.encode(
            encoding='utf_8'), response.get_data())

    def test_delete_auction_type(self):
        auction_type = AuctionType.query.first()
        auction_type_id = auction_type.id

        response = self.client.get(
            '/admin/auction/types/delete/' + str(auction_type.id))
        self.assertStatus(response, 302)

        self.assertIsNone(AuctionType.query.filter_by(
            id=auction_type_id).first())

    def test_delete_not_existing_auction_type(self):
        response = self.client.get('/admin/auction/types/delete/asdasd')
        self.assert_404(response)
