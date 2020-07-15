from django.test import TestCase
from django.db import IntegrityError

from rest_framework.test import APITestCase
from rest_framework import status

from .models import EventCategory, EventType


class EventCategoryTestCase(APITestCase):
    def setUp(self):
        EventCategory.objects.create(name='تکنولوژی')
        EventCategory.objects.create(name='پزشکی')
        EventCategory.objects.create(name='مارکت')

    def test_get_url(self):
        url1 = '/event/categories/'
        url2 = '/event/all-categories/'
        response1 = self.client.get(url1, format='json')
        response2 = self.client.get(url2, format='json')
        response3 = self.client.post(url2, format='json')
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_duplicate(self):
        with self.assertRaises(IntegrityError):
            EventCategory.objects.create(name='پزشکی')

    def test_db(self):
        qs1 = EventCategory.objects.all()
        self.assertEqual(qs1.count(), 3)
        qs2 = EventCategory.objects.filter(name='مارکت')
        self.assertTrue(qs2.exists())
        qs3 = EventCategory.objects.filter(name='شیمی')
        self.assertFalse(qs3.exists())

    def test_get_method(self):
        url = '/event/all-categories/'
        response = self.client.get(url)
        data = [{'id': 1, 'name': 'تکنولوژی', 'image': None}, {
            'id': 2, 'name': 'پزشکی', 'image': None}, {'id': 3, 'name': 'مارکت', 'image': None}]
        self.assertEqual(response.data, data)


class TypeTestCase(APITestCase):
    def setUp(self):
        EventType.objects.create(name='حضوری')
        EventType.objects.create(name='وبینار')
        EventType.objects.create(name='مجله')

    def test_get_url(self):
        url1 = '/event/types/'
        url2 = '/event/all-types/'
        response1 = self.client.get(url1, format='json')
        response2 = self.client.get(url2, format='json')
        response3 = self.client.post(url2, format='json')
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_duplicate(self):
        with self.assertRaises(IntegrityError):
            EventType.objects.create(name='حضوری')

    def test_db(self):
        qs1 = EventType.objects.all()
        self.assertEqual(qs1.count(), 3)
        qs2 = EventType.objects.filter(name='وبینار')
        self.assertTrue(qs2.exists())
        qs3 = EventType.objects.filter(name='دیگر')
        self.assertFalse(qs3.exists())

    def test_get_method(self):
        url = '/event/all-types/'
        response = self.client.get(url)
        data = [{'id': 1, 'name': 'حضوری'}, {
            'id': 2, 'name': 'وبینار'}, {'id': 3, 'name': 'مجله'}]
        self.assertEqual(response.data, data)
