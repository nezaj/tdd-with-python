from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape

from lists.forms import EMPTY_ITEM_ERROR, ItemForm
from lists.models import Item, List
from lists.views import home_page

class HomePageTest(TestCase):

    def test_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post('/lists/{}/'.format(list_.id), data={'text': ''})

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/{}/'.format(list_.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

    def test_invalid_input_saves_nothing_to_db(self):
        response = self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_passes_item_form(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_input_renders_form_errors(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')

class NewListTest(TestCase):

    def test_can_post_to_existing_list(self):
        correct_list = List.objects.create()

        self.client.post('/lists/{}/'.format(correct_list.id),
                         data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_post_redirects_to_list_view(self):
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/{}/'.format(correct_list.id),
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/{}/'.format(correct_list.id))

    def test_redirects_after_post(self):
        response = self.client.post('/lists/new',
                                    data={'text': 'A new list item'})

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))

    def test_save_after_post(self):
        self.client.post('/lists/new',
                         data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_validation_errors_shown_on_home(self):
        response = self.client.post('/lists/new', data={'text': ''})
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
