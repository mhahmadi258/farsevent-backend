from django.test import TestCase
from django.db import IntegrityError

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import EventCategory, EventType, Event, Ticket
from authapp.models import City


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


class EventCreateTestCase(APITestCase):
    def setUp(self):
        self.client.post('/auth/create/', {'username': 'mh1998',
                                           'email': 'mh1998@gmail.com',
                                           'password': 'Qw123456Qw'}, format='json')

        self.client.post('/auth/create/', {'username': 'rz1998',
                                           'email': 'rz1998@gmail.com',
                                           'password': 'Qw123456Qw'}, format='json')

        EventCategory.objects.create(name='cat1')
        EventType.objects.create(name='type1')
        City.objects.create(name='tehran')

    def get_clean_data(self):
        data = {
            'title': 'matlab',
            'image': None,
            'description': '...',
            'start_time': '2020-06-28T15:00:00Z',
            'end_time': '2020-06-28T18:00:00Z',
            'address': 'yeja',
            'tags': '#matblab',
            'event_type': 1,
            'event_category': 1,
            'city': 1,
            'tickets': 'kheyrie&khoob ast&20&20|kheyrie2&behtar ast&20&20'
        }
        return data

    def test_event_create_url(self):
        url1 = '/event/create/'
        url2 = '/event/create-event/'
        token = self.client.post(
            '/auth/login/', {'username': 'mh1998', 'password': 'Qw123456Qw'}).data.get('token')
        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response1 = self.client.post(url1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        response2 = self.client.post(url2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        response3 = auth_client.post(
            url2, self.get_clean_data(), format='json')
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)
        response4 = auth_client.get(url2)
        self.assertEqual(response4.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_requred_fields(self):
        url = '/event/create-event/'
        token = self.client.post(
            '/auth/login/', {'username': 'mh1998', 'password': 'Qw123456Qw'}).data.get('token')
        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response1 = auth_client.post(url, {}, format='json')
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(list(response1.data.keys()), [
                         'title', 'start_time', 'end_time', 'event_type', 'event_category', 'city', 'address', 'tickets'])
        data = self.get_clean_data()
        data['title'] = ''
        response2 = auth_client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        response3 = auth_client.post(url, self.get_clean_data(), format='json')
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

    def test_api(self):
        url = '/event/create-event/'
        token = self.client.post(
            '/auth/login/', {'username': 'mh1998', 'password': 'Qw123456Qw'}).data.get('token')
        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data =  self.get_clean_data()
        del data['tickets']
        response1 = auth_client.post(url, data, format='json')
        response2 = auth_client.post(url, self.get_clean_data(), format='json')

        self.assertEqual(Event.objects.all().count(), 1)
        self.assertAlmostEqual(Ticket.objects.all().count(), 2)


class EventTestCase(APITestCase):
    def setUp(self):
        self.client.post('/auth/create/', {'username': 'mh1998',
                                           'email': 'mh1998@gmail.com',
                                           'password': 'Qw123456Qw'}, format='json')

        EventCategory.objects.create(name='cat1')
        EventType.objects.create(name='type1')
        City.objects.create(name='tehran')
        token = self.client.post(
            '/auth/login/', {'username': 'mh1998', 'password': 'Qw123456Qw'}).data.get('token')
        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        data1 = self.get_clean_data()
        data2 = self.get_clean_data()
        data2['title'] = 'deep learning'

        auth_client.post('/event/create-event/', data1, format='json')
        auth_client.post('/event/create-event/', data2, format='json')

    def get_clean_data(self):
        data = {
            'title': 'matlab',
            'image': None,
            'description': '...',
            'start_time': '2020-06-28T15:00:00Z',
            'end_time': '2020-06-28T18:00:00Z',
            'address': 'yeja',
            'tags': '#matblab',
            'event_type': 1,
            'event_category': 1,
            'city': 1,
            'tickets': 'kheyrie&khoob ast&20&20|kheyrie2&behtar ast&20&20'
        }
        return data

    def test_url(self):
        url1 = '/event/event-list/'
        url2 = '/event/event/1/'
        url3 = '/event/event/2/'
        url4 = 'event/event/3/'
        url5 = '/event/event-lists/'

        response1 = self.client.get(url1)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.client.get(url3)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        response4 = self.client.get(url4)
        self.assertEqual(response4.status_code, status.HTTP_404_NOT_FOUND)
        response5 = self.client.get(url5)
        self.assertEqual(response5.status_code, status.HTTP_404_NOT_FOUND)
        response6 = self.client.post(url1)
        self.assertEqual(response6.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        response7 = self.client.post(url2)

    def test_api(self):
        url1 = '/event/event-list/'
        url2 = '/event/event/1/'
        response1 = self.client.get(url1)
        self.assertEqual(response1.data, [{'id': 1, 'title': 'matlab', 'image': None}, {
                         'id': 2, 'title': 'deep learning', 'image': None}])
        response2 = self.client.get(url2)
        self.assertEqual(list(response2.data.keys()), ['id', 'title', 'image', 'description', 'start_time',
                                                       'end_time', 'tags', 'event_type', 'event_category', 'city', 'address', 'tickets'])
