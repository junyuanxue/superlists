from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_url(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Get Python stickers'
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'Get Python stickers')
        self.assertIn('Get Python stickers', response.content.decode())

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'Get Python stickers'},
            request=request
        )
        self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):

    def add_item(self, text):
        item = Item()
        item.text = text
        item.save()

    def test_saving_and_retrieving_items(self):
        self.add_item('Le premier')
        self.add_item('Le deuxieme')
        items = Item.objects.all()
        self.assertEqual(items.count(), 2)
        self.assertEqual(items[0].text, 'Le premier')
        self.assertEqual(items[1].text, 'Le deuxieme')
