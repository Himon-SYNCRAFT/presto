from flask import Flask
from flask.ext.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from presto import app, models
from presto.tests.base import BaseTestCase
from presto.database import db_session, Base
from sqlalchemy import create_engine
import unittest


class UserManagementTest(LiveServerTestCase):

    def create_app(self):
        app.config.from_object('presto.settings.TestConfig')
        self.live_server_url = 'http://localhost:' + \
            str(app.config['LIVESERVER_PORT'])
        self.test_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        db_session.configure(bind=self.test_engine)

        return app

    def setUp(self):
        Base.metadata.create_all(self.test_engine)

        user = models.User('danzaw', 'danzaw@mail.pl', "it's a secret")
        user2 = models.User('himon', 'himon@mail.pl', "it's a secret")

        db_session.add(user)
        db_session.add(user2)
        db_session.commit()

        account = models.Account('danzaw', 'danzaw@gmail.com',
                                 "it's a secret", 'webapi_key')

        db_session.add(account)
        db_session.commit()

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(30)

    def tearDown(self):
        db_session.remove()
        Base.metadata.reflect(self.test_engine)
        Base.metadata.drop_all(self.test_engine)

        self.browser.quit()

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

        response = self.browser.get(self.live_server_url + '/admin/users')

        new_user_button = self.browser.find_element_by_id('add-user')
        new_user_button.click()

        self.assertIn('name="login"', self.browser.page_source)
        self.assertIn('name="mail"', self.browser.page_source)
        self.assertIn('name="password"', self.browser.page_source)
        self.assertIn('name="submit"', self.browser.page_source)

        login_input = self.browser.find_element_by_name('login')
        mail_input = self.browser.find_element_by_name('mail')
        password_input = self.browser.find_element_by_name('password')
        submit = self.browser.find_element_by_name('submit')

        login_input.send_keys('user1234567')
        mail_input.send_keys('mail_input2@wp.pl')
        password_input.send_keys('pass123456')
        submit.click()

        td = self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('td')

        self.assertIn('user1234567', [item.text for item in td])
        self.assertIn('mail_input2@wp.pl', [item.text for item in td])
        self.assertNotIn('pass123456', [item.text for item in td])

    def test_edit_user(self):
        response = self.browser.get(self.live_server_url + '/admin/users')
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
        submit = self.browser.find_element_by_name('submit')

        self.assertEqual(login_input.get_attribute('value'), user.login)
        self.assertEqual(mail_input.get_attribute('value'), user.mail)

        login_input.clear()
        mail_input.clear()

        login_input.send_keys('user7654321')
        mail_input.send_keys('mail_input99@wp.pl')
        submit.click()

        td = self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('td')

        self.assertIn('user7654321', [item.text for item in td])
        self.assertIn('mail_input99@wp.pl', [item.text for item in td])

    # def test_change_password(self):
    #     pass

    def test_delete_user(self):
        # Jest na stronie zarzadzania uzytkownikami
        # Klikam na przycisk usuwania 1 uzytkowika
        # Lista uzytkownikow sie przeladowuje
        # Nie ma juz na liscie uzytkownika, ktorego usunalem

        response = self.browser.get(self.live_server_url + '/admin/users')
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


class ShippingTypeTestCase(LiveServerTestCase):

    def create_app(self):
        app.config.from_object('presto.settings.TestConfig')
        self.live_server_url = 'http://localhost:' + \
            str(app.config['LIVESERVER_PORT'])
        self.test_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        db_session.configure(bind=self.test_engine)

        return app

    def setUp(self):
        Base.metadata.create_all(self.test_engine)

        user = models.User('danzaw', 'danzaw@mail.pl', "it's a secret")
        user2 = models.User('himon', 'himon@mail.pl', "it's a secret")

        db_session.add(user)
        db_session.add(user2)
        db_session.commit()

        account = models.Account('danzaw', 'danzaw@gmail.com',
                                 "it's a secret", 'webapi_key')

        db_session.add(account)
        db_session.commit()

        shipping_type1 = models.ShippingType('Kurier', False)
        shipping_type2 = models.ShippingType('Odbiór osobisty', True)

        db_session.add(shipping_type1)
        db_session.add(shipping_type2)

        db_session.commit()

        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(30)

    def tearDown(self):
        db_session.remove()
        Base.metadata.reflect(self.test_engine)
        Base.metadata.drop_all(self.test_engine)

        self.browser.quit()

    def test_shipping_type_management(self):
        self.browser.get(self.live_server_url + '/admin/shipping/types')

        table = self.browser.find_element_by_id('shipping-types-list')
        anchors = table.find_elements_by_tag_name('a')

        self.assertTrue(any([item.get_attribute('href'.startswith(
            '/admin/shipping/types/delete')) for item in anchors]))

        self.assertTrue(any([item.get_attribute('href'.startswith(
            '/admin/shipping/types/edit')) for item in anchors]))

        anchors = self.browser.find_elements_by_tag_name('a')

        self.assertTrue(any([item.get_attribute('href') ==
                             'admin/shipping/types/add' for item in anchors]))

    def test_add_shipping_type(self):
        self.browser.get(self.live_server_url + '/admin/shipping/types')

        table = self.browser.find_element_by_id('shipping-types-list')
        add_button = self.browser.find_element_by_id('add-shipping-type')

        add_button.click()

        name_input = self.browser.find_element_by_name('name')
        is_boolean_input = self.browser.find_element_by_name('is_boolean')

        name_input.send_keys('Kurier')
        is_boolean_input.click()

        save_button = self.browser.find_elements('submit')

        save_button.click()

        table = self.browser.find_element_by_id('shipping-types-list')
        td = table.find_elements_by_tag_name('td')

        self.assertIn('Kurier', [t.text for t in td])


    # def edit_shipping_type(self):
    #     pass
    #
    # def delete_shipping_type(self):
    #     pass
