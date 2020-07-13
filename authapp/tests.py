from django.test import TestCase
from django.db import IntegrityError

from rest_framework.test import APITestCase
from rest_framework import status

from .models import City  

class CityTestCase(APITestCase):
    def setUp(self):
        City.objects.create(name='تهران')
        City.objects.create(name='شیراز')
        City.objects.create(name='اصفهان')

    def test_get_url(self):
        url1 = 'http://localhost:8000/auth/cities/'
        url2 = 'http://localhost:8000/auth/all-cities/'
        response1 = self.client.get(url1,format = 'json')
        response2 = self.client.get(url2,format = 'json')
        self.assertEqual(response1.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code,status.HTTP_200_OK)

    def test_duplicate(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name='تهران')

    def test_db(self):
        qs1 = City.objects.all()
        self.assertEqual(qs1.count(),3)
        qs2 = City.objects.filter(name='شیراز')
        self.assertTrue(qs2.exists())
        qs3 = City.objects.filter(name='رشت')
        self.assertFalse(qs3.exists())

    def test_get_method(self):
        url = 'http://localhost:8000/auth/all-cities/'
        response = self.client.get(url)
        data = [{'id': 1 ,'name':'تهران'},{'id': 2 ,'name':'شیراز'},{'id': 3 ,'name':'اصفهان'}]
        self.assertEqual(response.data,data)
        