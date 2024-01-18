from django.test import TestCase
from django.urls import reverse
from django.test import Client
# Create your tests here.
client = Client()


class IndexViewTest(TestCase):
    def test_if_accessible(self):
        response = self.client.get(reverse('memory-index'))
        self.assertEqual(response.status_code, 200)
