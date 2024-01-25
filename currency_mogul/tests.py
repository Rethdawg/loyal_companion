from django.test import TestCase
from django.test import Client
from django.urls import reverse
import numpy as np
# Create your tests here.
client = Client()


class IndexViewTests(TestCase):
    def test_default_view(self):
        """
        Testing to see if the page is available.
        :return:None
        """
        response = self.client.get(reverse('currency-index'))
        self.assertEqual(response.status_code, 200)


class HistoricalViewTests(TestCase):
    def test_if_no_graph(self):
        """
        Testing to see if the page doesn't load an old graph.
        :return:None
        """
        response = self.client.get(reverse('currency-historical'))
        self.assertContains(response, 'Generate a graph!', status_code=200)

    def test_if_graph(self):
        """
        Testing to see if the page accepts the context and displays it.
        :return:None
        """
        test_context = {
            'from_curr': 'EUR',
            'to_curr': 'USD',
            'amount': 100,
            'from_date': np.datetime64('2024-01-01'),
            'to_date': np.datetime64('2024-01-14'),
            'posting': True,
        }
        response = self.client.post(reverse('currency-historical'), data=test_context)
        self.assertContains(response,
                            f'{test_context["amount"]} {test_context["from_curr"]} - {test_context["to_curr"]}, '
                            f'{test_context["from_date"]} - {test_context["to_date"]}',
                            status_code=200)


class ConverterViewTest(TestCase):
    def test_if_converts(self):
        """
        Checking to see if the conversion goes through.
        :return:None
        """
        test_context = {
            'from_curr': 'EUR',
            'to_curr': 'USD',
            'amount': 100,
        }
        response = self.client.post(reverse('currency-converter'), data=test_context)
        self.assertEquals(response.status_code, 200)
