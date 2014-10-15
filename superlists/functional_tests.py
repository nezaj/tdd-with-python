#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

        # Wait up to three seconds for the page to load
        # Later on we will want to change this to use a more sophisicated waiting algorithim
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_row_in_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_start_and_retrieve_list(self):
        # Edith goes to home page
        self.browser.get('http://localhost:8000')

        # She sees mention of to-do in page title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # There is an input area for her to type in a To-do
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # She types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # the page updates, and shows the item in her to-do list
        self.check_row_in_table('1: Buy peacock feathers')

        # There is still an input area for her to type more To-dos
        inputbox = self.browser.find_element_by_id('id_new_item')

        # She types "Buy more peacock feathers" and hits enter
        inputbox.send_keys('Buy more peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # The page updates, and shows both items in her to-do list
        self.check_row_in_table('1: Buy peacock feathers')
        self.check_row_in_table('2: Buy more peacock feathers')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')
