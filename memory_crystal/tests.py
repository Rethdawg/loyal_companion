import datetime
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .models import Birthday
from django.contrib import messages
# Create your tests here.
client = Client()


class IndexViewTest(TestCase):
    def test_if_accessible(self):
        response = self.client.get(reverse('memory-index'))
        self.assertEqual(response.status_code, 200)


class RenewBirthdayTest(TestCase):
    def test_if_renews(self):
        birthday1 = Birthday(person='John', bdate=datetime.date(2024, 1, 18))
        birthday1.renew_birthday()
        self.assertEqual(birthday1.bdate.year, 2025)

    def test_if_renew_saves(self):
        Birthday.objects.create(person='John', bdate=datetime.date(2024, 1, 18))
        for obj in Birthday.objects.all():
            obj.renew_birthday()
        queried_birthday = Birthday.objects.filter(person__contains='John').all()
        for obj in queried_birthday:
            self.assertEqual(obj.bdate.year, 2025)


class TestBirthdayAlerts(TestCase):
    def test_alert_user_28(self):
        Birthday.objects.create(person='John',
                                bdate=datetime.date.today() + datetime.timedelta(days=27))
        response = self.client.get(reverse('memory-index'))
        for obj in Birthday.objects.all():
            obj.alert_user(response)
        self.assertContains(response, 'John\'s birthday is coming up soon!')

    def test_alert_user_13(self):
        Birthday.objects.create(person='John',
                                bdate=datetime.date.today() + datetime.timedelta(days=13))
        response = self.client.get(reverse('memory-index'))
        for obj in Birthday.objects.all():
            obj.alert_user(response)
        self.assertContains(response,
                            f'John\'s birthday is coming up on the '
                            f'{datetime.date.today() + datetime.timedelta(days=13)}!!')
    def test_alert_user_1(self):
        Birthday.objects.create(person='John',
                                bdate=datetime.date.today() + datetime.timedelta(days=1))
        response = self.client.get(reverse('memory-index'))
        for obj in Birthday.objects.all():
            obj.alert_user(response)
        self.assertContains(response, f'John\'s birthday is tomorrow!')

    def test_alert_user_0(self):
        Birthday.objects.create(person='John',
                                bdate=datetime.date.today())
        response = self.client.get(reverse('memory-index'))
        for obj in Birthday.objects.all():
            obj.alert_user(response)
        self.assertContains(response,f'!!!John\'s birthday is today!!!')


