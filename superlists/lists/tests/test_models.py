from django.core.exceptions import ValidationError
from django.test import TestCase

from lists.models import Item, List

class ItemModelTest(TestCase):

    def test_blank_items_are_invalid(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_CAN_save_same_item_to_diff_list(self):
        list_1 = List.objects.create()
        Item.objects.create(text='Moop', list=list_1)
        list_2 = List.objects.create()
        item = Item(text='Moop', list=list_2)
        item.full_clean()  # Should not raise error

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='Moop', list=list_)
        with self.assertRaises(ValidationError):
            item = Item(text='Moop', list=list_)
            item.full_clean()

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text='Moop')
        self.assertIn(item, list_.item_set.all())

    def test_item_ordering(self):
        """Items should be ordered by id"""
        list_ = List.objects.create()
        item1 = Item.objects.create(list=list_, text='i1')
        item2 = Item.objects.create(list=list_, text='2')
        item3 = Item.objects.create(list=list_, text='3')

        item_query_list = list(Item.objects.all())
        items = [item1, item2, item3]
        self.assertEqual(item_query_list, items)

    def test_str_repr(self):
        item = Item(text='Moop')
        self.assertEqual(str(item), 'Moop')

class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/{}/'.format(list_.id))
