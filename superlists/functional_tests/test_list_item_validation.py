from unittest import skip

from .base import FunctionalTest
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, EMPTY_ITEM_ERROR)

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_row_in_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys('\n')

        # She receives a similar warning on the list page
        self.check_row_in_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, EMPTY_ITEM_ERROR)

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_row_in_table('1: Buy milk')
        self.check_row_in_table('2: Make tea')

    def test_cannot_add_duplicate_item(self):
        # Edith goes to home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_row_in_table('1: Buy milk')

        # She tries to add a duplicate item
        self.get_item_input_box().send_keys('Buy milk\n')

        # She gets a helpful error message
        self.check_row_in_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, DUPLICATE_ITEM_ERROR)

        # So she adds a different item
        self.get_item_input_box().clear()
        self.get_item_input_box().send_keys('Buy cheese\n')
        self.check_row_in_table('1: Buy milk')
        self.check_row_in_table('2: Buy cheese')
