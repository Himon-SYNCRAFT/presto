from flask.ext.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from sqlalchemy import create_engine
from presto import app, models
from presto.database import db_session, Base
from presto.tests.base import LiveServerBaseTestCase


class UserManagementTest(LiveServerBaseTestCase):

    def test_user_management_page(self):
        # Przechodze do panelu zarzadzania uzytkownikami
        # Widze liste uzytkownikow
        # Na liscie znajduja sie przyciski edytuj, usun
        # Mozemy tez dodac nowego uzytkonika za pomoca przycisku nowy

        self.browser.get(self.live_server_url + '/admin/users')

        table = self.browser.find_element_by_id('users-list')
        table_anchors = table.find_elements_by_tag_name('a')
        anchors = self.browser.find_elements_by_tag_name('a')

        self.assertTrue(any([item.get_attribute("href").startswith(
            self.live_server_url + '/admin/users/add') for item in anchors]))
        self.assertTrue(any([item.get_attribute("href").startswith(
            self.live_server_url + '/admin/users/edit') for item in table_anchors]))
        self.assertTrue(any([item.get_attribute("href").startswith(
            self.live_server_url + '/admin/users/delete') for item in table_anchors]))

    def test_add_new_user(self):
        # Przechodze do panelu zarzadzania uzytkownikami
        # Widze liste uzytkownikow
        # Wciskam przycisk odpowiadajacy za dodanie nowego uzytkownikami
        # Przechodze do formularza w ktorym znajduja sie pola na login, mail i haslo
        # uzupelniam dane i klikam przycisk zapisz
        # strone sie przeladowuje i znowu pokazuje liste uzytkownikow rozszerzona
        # o tego ktorego wprowadzilem

        self.browser.get(self.live_server_url + '/admin/users')

        new_user_button = self.browser.find_element_by_id('add-user')
        new_user_button.click()

        self.assertIn('name="login"', self.browser.page_source)
        self.assertIn('name="mail"', self.browser.page_source)
        self.assertIn('name="password"', self.browser.page_source)
        self.assertIn('name="role"', self.browser.page_source)
        self.assertIn('name="submit"', self.browser.page_source)

        login_input = self.browser.find_element_by_name('login')
        mail_input = self.browser.find_element_by_name('mail')
        password_input = self.browser.find_element_by_name('password')
        role_input = Select(self.browser.find_element_by_name('role'))
        submit = self.browser.find_element_by_name('submit')

        login_input.send_keys('user1234567')
        mail_input.send_keys('mail_input2@wp.pl')
        password_input.send_keys('pass123456')
        role_input.select_by_visible_text('admin')
        submit.click()

        td = self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('td')

        self.assertIn('user1234567', [item.text for item in td])
        self.assertIn('mail_input2@wp.pl', [item.text for item in td])
        self.assertIn('admin', [item.text for item in td])
        self.assertNotIn('pass123456', [item.text for item in td])

    def test_edit_user(self):
        self.browser.get(self.live_server_url + '/admin/users')
        user = models.User.query.first()

        td = self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('td')
        self.assertIn(user.login, [item.text for item in td])

        table = self.browser.find_element_by_id('users-list')

        edit_user_url = '/admin/users/edit/' + str(user.id)
        edit_button_xpath = "//a[@href='{}']".format(edit_user_url)
        edit_button = table.find_element_by_xpath(edit_button_xpath)

        edit_button.click()

        login_input = self.browser.find_element_by_name('login')
        mail_input = self.browser.find_element_by_name('mail')
        role_input = Select(self.browser.find_element_by_name('role'))
        submit = self.browser.find_element_by_name('submit')

        self.assertEqual(login_input.get_attribute('value'), user.login)
        self.assertEqual(mail_input.get_attribute('value'), user.mail)

        login_input.clear()
        mail_input.clear()

        login_input.send_keys('user7654321')
        mail_input.send_keys('mail_input99@wp.pl')
        role_input.select_by_visible_text('admin')
        submit.click()

        td = self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('td')

        self.assertIn('user7654321', [item.text for item in td])
        self.assertIn('mail_input99@wp.pl', [item.text for item in td])
        self.assertIn('admin', [item.text for item in td])

    # def test_change_password(self):
    #     pass

    def test_delete_user(self):
        # Jest na stronie zarzadzania uzytkownikami
        # Klikam na przycisk usuwania 1 uzytkowika
        # Lista uzytkownikow sie przeladowuje
        # Nie ma juz na liscie uzytkownika, ktorego usunalem

        self.browser.get(self.live_server_url + '/admin/users')
        user = models.User.query.first()

        td = self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('td')
        self.assertIn(user.login, [item.text for item in td])

        table = self.browser.find_element_by_id('users-list')

        delete_user_url = '/admin/users/delete/' + str(user.id)
        delete_button_xpath = "//a[@href='{}']".format(delete_user_url)
        delete_button = table.find_element_by_xpath(delete_button_xpath)

        delete_button.click()

        td = self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('td')
        self.assertNotIn(user.login, [item.text for item in td])


class ShippingTypeTestCase(LiveServerBaseTestCase):

    def test_shipping_type_management(self):
        self.browser.get(self.live_server_url + '/admin/shipping/types')

        table = self.browser.find_element_by_id('shipping-types-list')
        anchors = table.find_elements_by_tag_name('a')

        self.assertTrue(any([item.get_attribute('href').startswith(
            self.live_server_url + '/admin/shipping/types/delete') for item in anchors]))

        self.assertTrue(any([item.get_attribute('href').startswith(
            self.live_server_url + '/admin/shipping/types/edit') for item in anchors]))

        anchors = self.browser.find_elements_by_tag_name('a')

        self.assertTrue(any([(item.get_attribute('href') ==
                              self.live_server_url + '/admin/shipping/types/add') for item in anchors]))

    def test_add_shipping_type(self):
        self.browser.get(self.live_server_url + '/admin/shipping/types')

        table = self.browser.find_element_by_id('shipping-types-list')
        add_button = self.browser.find_element_by_id('add-shipping-type')

        add_button.click()

        name_input = self.browser.find_element_by_name('name')
        is_boolean_input = self.browser.find_element_by_name('is_boolean')

        name_input.send_keys('Packomat')
        is_boolean_input.click()

        save_button = self.browser.find_element_by_name('submit')

        save_button.click()

        table = self.browser.find_element_by_id('shipping-types-list')
        td = table.find_elements_by_tag_name('td')

        self.assertIn('Packomat', [t.text for t in td])

    def edit_shipping_type(self):
        shipping_type = models.ShippingType.query.first()

        self.browser.get(self.live_server_url + '/admin/shipping/types')

        table = self.browser.find_element_by_id('shipping-types-list')

        edit_url = '/admin/shipping/types/edit/' + str(shipping_type.id)
        edit_button_xpath = "//a[@href='{}']".format(edit_url)
        edit_button = table.find_element_by_xpath(edit_button_xpath)

        edit_button.click()

        name_input = self.browser.find_element_by_name('name')
        is_boolean_input = self.browser.find_element_by_name('is_boolean')

        name_input.clear()
        name_input.send_keys('Paczkomat123')
        is_boolean_input.click()

        save_button = self.browser.find_element_by_name('submit')

        save_button.click()

        table = self.browser.find_element_by_id('shipping-types-list')
        td = table.find_elements_by_tag_name('td')

        self.assertIn('Paczkomat123', [t.text for t in td])

    def delete_shipping_type(self):
        shipping_type = models.ShippingType.query.first()

        self.browser.get(self.live_server_url + '/admin/shipping/types')

        table = self.browser.find_element_by_id('shipping-types-list')

        url = '/admin/shipping/types/delete/' + str(shipping_type.id)
        button_xpath = "//a[@href='{}']".format(url)
        button = table.find_element_by_xpath(button_xpath)

        button.click()

        table = self.browser.find_element_by_id('shipping-types-list')
        td = table.find_elements_by_tag_name('td')

        self.assertNotIn(shipping_type.name, [t.text for t in td])


class AuctionTypeTestCase(LiveServerBaseTestCase):

    def test_auction_type_page_exist(self):
        self.browser.get(self.live_server_url + '/admin/auction/types')

        table = self.browser.find_element_by_id('auction-types-list')

        anchors = table.find_elements_by_tag_name('a')

        self.assertTrue(any([item.get_attribute('href').startswith(
            self.live_server_url + '/admin/auction/types/delete') for item in anchors]))

        self.assertTrue(any([item.get_attribute('href').startswith(
            self.live_server_url + '/admin/auction/types/edit') for item in anchors]))

        anchors = self.browser.find_elements_by_tag_name('a')

        self.assertTrue(any([(item.get_attribute('href') ==
                              self.live_server_url + '/admin/auction/types/add') for item in anchors]))

    def test_add_auction_type(self):
        self.browser.get(self.live_server_url + '/admin/auction/types')

        td = self.browser.find_elements_by_tag_name('td')
        self.assertNotIn('niezwykła', [item.text for item in td])

        add_button = self.browser.find_element_by_id('add-auction-type')
        add_button.click()

        name_input = self.browser.find_element_by_name('name')
        name_input.send_keys('niezwykła')

        submit_button = self.browser.find_element_by_name('submit')
        submit_button.click()

        td = self.browser.find_elements_by_tag_name('td')
        self.assertIn('niezwykła', [item.text for item in td])

    def test_edit_auction_type(self):
        auction_type = models.AuctionType.query.first()
        self.browser.get(self.live_server_url + '/admin/auction/types')

        table = self.browser.find_element_by_id('auction-types-list')

        edit_url = '/admin/auction/types/edit/' + str(auction_type.id)
        edit_button_xpath = "//a[@href='{}']".format(edit_url)
        edit_button = table.find_element_by_xpath(edit_button_xpath)

        edit_button.click()

        name_input = self.browser.find_element_by_name('name')

        name_input.clear()
        name_input.send_keys('niezywkła')

        save_button = self.browser.find_element_by_name('submit')

        save_button.click()

        table = self.browser.find_element_by_id('auction-types-list')
        td = table.find_elements_by_tag_name('td')

        self.assertIn('niezywkła', [t.text for t in td])

    def test_delete_auction_type(self):
        auction_type = models.AuctionType.query.first()
        self.browser.get(self.live_server_url + '/admin/auction/types')

        table = self.browser.find_element_by_id('auction-types-list')

        url = '/admin/auction/types/delete/' + str(auction_type.id)
        button_xpath = "//a[@href='{}']".format(url)
        button = table.find_element_by_xpath(button_xpath)

        button.click()

        table = self.browser.find_element_by_id('auction-types-list')
        td = table.find_elements_by_tag_name('td')

        self.assertNotIn(auction_type.name, [t.text for t in td])
