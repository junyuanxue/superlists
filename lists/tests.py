from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_url(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item-text'] = 'Get Python stickers'
        response = home_page(request)
        self.assertIn('Get Python stickers', response.content.decode())

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'Get Python stickers'}
        )
        self.assertEqual(response.content.decode(), expected_html)
