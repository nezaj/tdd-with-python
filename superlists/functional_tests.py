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

    def test_start_and_retrieve_list(self):
        # Edith goes to home page
        self.browser.get('http://localhost:8000')

        # Edith sees mention of to-do in page title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # There is an input area for Edith to type in a To-do
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # Edit types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When Edith hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feather', [row.text for row in rows])

        # There is still an input area for Edith to type more To-dos
        inputbox = self.browser.find_element_by_id('id_new_item')

        # Edith types "Buy more peacock feathers" and hits enter
        inputbox.send_keys('Buy more peacock feathers')
        inputbox.send_keys(Keys.ENTER)

        # The page updates, and shows both items in her to-do list
        self.assertIn('1: Buy peacock feather', [row.text for row in rows])
        self.assertIn('2: Buy more peacock feathers', [row.text for row in rows])

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')
