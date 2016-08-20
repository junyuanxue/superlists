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

    def test_returns_correct_url(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', request=request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_saves_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Get Python stickers'
        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.first().text, 'Get Python stickers')

    def test_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Get Python stickers'
        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

    def test_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

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

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_display_all_items(self):
        Item.objects.create(text='Un')
        Item.objects.create(text='Deux')
        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Un')
        self.assertContains(response, 'Deux')
