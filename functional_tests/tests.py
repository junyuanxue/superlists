from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element_by_id('new-item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        input_box.send_keys('Get Rails stickers')
        input_box.send_keys(Keys.ENTER)
        luke_list_url = self.browser.current_url
        self.assertRegex(luke_list_url, '/lists/.+')
        
        table = self.browser.find_element_by_id('list-table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Get Rails stickers', [row.text for row in rows])

        input_box = self.browser.find_element_by_id('new-item')
        input_box.send_keys('Get Django stickers')
        input_box.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('list-table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Get Rails stickers', [row.text for row in rows])
        self.assertIn('2: Get Django stickers', [row.text for row in rows])

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Get Rails stickers', page_text)
        self.assertNotIn('Get Django stickers', page_text)

        input_box.self.browser.find_element_by_id('new-item')
        input_box.send_keys('Read Harry Potter')
        input_box.send_keys(Keys.ENTER)

        han_list_url = self.browser.current_url
        self.assertRegex(han_list_url, '/lists/.+')
        self.assertNotEqual(han_list_url, luke_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Get Rails stickers', page_text)
        self.assertNotIn('Get Django stickers', page_text)
