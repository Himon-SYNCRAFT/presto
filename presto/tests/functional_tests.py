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

    def setUp(self):
        self.test_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

        db_session.configure(bind=self.test_engine)
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
        Base.metadata.drop_all(self.test_engine)

        self.browser.quit()

    def create_app(self):
        app.config.from_object('presto.settings.TestConfig')
        self.live_server_url = 'http://localhost:' + \
            str(app.config['LIVESERVER_PORT'])
        return app

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
        rows_count = len(self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('tr'))

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

        login_input.send_keys('user123456')
        mail_input.send_keys('mail_input@wp.pl')
        password_input.send_keys('pass123456')
        submit.click()

        rows_count_after_add_new_user = len(self.browser.find_element_by_id(
            'users-list').find_elements_by_tag_name('tr'))

        self.assertIs(rows_count_after_add_new_user, rows_count + 1)
