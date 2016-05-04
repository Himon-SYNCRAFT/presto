from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class UserManagementTest(unittest.TestCase):

    live_server_url = 'http://localhost:5000'

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
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

        self.assertTrue(any([item.get_attribute("href").startswith(self.live_server_url + '/admin/users/add') for item in anchors]))
        self.assertTrue(any([item.get_attribute("href").startswith(self.live_server_url + '/admin/users/edit') for item in table_anchors]))
        self.assertTrue(any([item.get_attribute("href").startswith(self.live_server_url + '/admin/users/delete') for item in table_anchors]))

    def test_add_new_user(self):
        # Przechodze do panelu zarzadzania uzytkownikami
        # Widze liste uzytkownikow
        # Wciskam przycisk odpowiadajacy za dodanie nowego uzytkownikami
        # Przechodze do formularza w ktorym znajduja sie pola na login, mail i haslo
        # uzupelniam dane i klikam przycisk zapisz
        # strone sie przeladowuje i znowu pokazuje liste uzytkownikow rozszerzona
        # o tego ktorego wprowadzilem

        self.browser.get(self.live_server_url + '/admin/users')
        rows_count = len(self.browser.find_element_by_id('users-list').find_elements_by_tag_name('tr'))

        new_user_button = self.browser.find_element_by_id('add-user')
        new_user_button.click()

        login_input = self.browser.find_element_by_name('login')
        mail_input = self.browser.find_element_by_name('mail')
        password_input = self.browser.find_element_by_name('password')
        submit = self.browser.find_element_by_name('submit')

        login_input.send_keys('user1')
        mail_input.send_keys('mail_input@wp.pl')
        password_input.send_keys('pass')
        submit.click()

        rows_count_after_add_new_user = len(self.browser.find_element_by_id('users-list').find_elements_by_tag_name('tr'))

        self.assertIs(rows_count_after_add_new_user, rows_count + 1)







if __name__ == '__main__':
    unittest.main()
