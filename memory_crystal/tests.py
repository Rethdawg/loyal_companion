import datetime
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .models import Birthday
# Create your tests here.
client = Client()


class IndexViewTest(TestCase):
    """
    Tests relating to the index view.
    """
    def test_if_accessible(self):
        """
        Checks if the index view is accessible.
        :return: None
        """
        response = self.client.get(reverse('memory-index'))
        self.assertEqual(response.status_code, 200)


class RenewBirthdayTest(TestCase):
    """
    Tests relating to the .renew_birthday() method of the Birthday model.
    """
    def test_if_renews(self):
        """
        Test to see if the renew_birthday() successfully increments the bdate of a Birthday instance.
        :return: None
        """
        birthday1 = Birthday(person='John', bdate=datetime.date(2024, 1, 18))
        birthday1.renew_birthday()
        self.assertEqual(birthday1.bdate.year, 2025)

    def test_if_renew_saves(self):
        """
        Test to see if the increment of the renew_birthday() method is saved to the database.
        :return: None
        """
        Birthday.objects.create(person='John', bdate=datetime.date(2024, 1, 18))
        for obj in Birthday.objects.all():
            obj.renew_birthday()
        queried_birthday = Birthday.objects.filter(person__contains='John').all()
        for obj in queried_birthday:
            self.assertEqual(obj.bdate.year, 2025)
