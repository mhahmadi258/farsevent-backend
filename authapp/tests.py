from django.test import TestCase
from django.db import IntegrityError

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import User, City


class UserTestCase(APITestCase):
    def setUp(self):
        data_sample1 = {'username': 'mh1998',
                        'password': 'Qw123456', 'email': 'mh1998@gmail.com'}
        data_sample2 = {'username': 'al1998',
                        'password': 'Qw123456', 'email': 'al1998@gmail.com'}
        data_sample3 = {'username': 'rz1998',
                        'password': 'Qw654321', 'email': 'rz1998@gmail.com'}
        User.objects.create(**data_sample1)
        User.objects.create(**data_sample2)
        User.objects.create(**data_sample3)

    def test_post_url(self):
        data = {'username': 'qw1234', 'password': 'Qw654Mh321Qw',
                'email': 'qw1234@yahoo.com'}
        correct_url = '/auth/create/'
        wrong_url = '/auth/creates/'
        response1 = self.client.post(wrong_url, format='json')
        response2 = self.client.post(wrong_url, data, format='json')
        response3 = self.client.post(correct_url, format='json')
        response4 = self.client.post(correct_url, data, format='json')
        response5 = self.client.get(correct_url, format='json')
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response5.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_required_fields(self):
        url = '/auth/create/'
        sample_data1 = {'password': 'Qw123456', 'email': 'wp1234@yahoo.com'}
        sample_data2 = {'username': 'wp1234', 'email': 'wp1234@yahoo.com'}
        sample_data3 = {'username': 'wp1234', 'password': 'Qw123456'}
        sample_data4 = {'username': 'wp1234'}
        sample_data5 = {'username': 'wp1234',
                        'password': 'Qw123456Qw', 'email': 'wp1234@yahoo.com'}

        error_data1 = {'username': ['This field is required.']}
        error_data2 = {'password': ['This field is required.']}
        error_data3 = {'email': ['This field is required.']}
        error_data4 = {'email': ['This field is required.'],
                       'password': ['This field is required.']}

        response1 = self.client.post(url, sample_data1, format='json')
        response2 = self.client.post(url, sample_data2, format='json')
        response3 = self.client.post(url, sample_data3, format='json')
        response4 = self.client.post(url, sample_data4, format='json')
        response5 = self.client.post(url, sample_data5, format='json')

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response1.data, error_data1)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data, error_data2)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.data, error_data3)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response4.data, error_data4)
        self.assertEqual(response5.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 4)
        self.assertTrue(User.objects.filter(username='wp1234').exists())

    def test_validators(self):
        url = '/auth/create/'
        sample_data1 = {'username': 'wp1234*',
                        'password': 'Qw123456Qw', 'email': 'wp1234@yahoo.com'}
        sample_data2 = {'username': 'wp1234',
                        'password': 'Qw123456Qw', 'email': 'wp1234yahoo.com'}
        sample_data3 = {'username': 'wp1234',
                        'password': '192837', 'email': 'wp1234@yahoo.com'}

        respons1 = self.client.post(url, sample_data1, format='json')
        self.assertEqual(respons1.status_code, status.HTTP_400_BAD_REQUEST)
        respons2 = self.client.post(url, sample_data2, format='json')
        self.assertEqual(respons2.status_code, status.HTTP_400_BAD_REQUEST)
        respons3 = self.client.post(url, sample_data3, format='json')
        self.assertEqual(respons3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 3)

    def test_duplicate(self):
        url = '/auth/create/'
        data_sample1 = {'username': 'mh1998',
                        'password': 'Qw123456', 'email': 'mh19988@gmail.com'}
        data_sample2 = {'username': 'mh19988',
                        'password': 'Qw123456', 'email': 'mh1998@gmail.com'}
        data_sample3 = {'username': 'mh1998',
                        'password': 'Qw123456', 'email': 'mh1998@gmail.com'}

        respons1 = self.client.post(url, data_sample1, format='json')
        self.assertEqual(respons1.status_code,status.HTTP_400_BAD_REQUEST)
        respons2 = self.client.post(url, data_sample2, format='json')
        self.assertEqual(respons2.status_code,status.HTTP_400_BAD_REQUEST)
        respons3 = self.client.post(url, data_sample3, format='json')
        self.assertEqual(respons3.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(),3)
        

    def test_api(self):
        url = '/auth/create/'
        sample_data1 = {'username': 'wp1234',
                        'password': 'Qw123456Qw', 'email': 'wp1234@yahoo.com'}
        response = self.client.post(url, sample_data1, format='json')
        user = User.objects.get(username='wp1234')
        token = Token.objects.get(user=user).key
        self.assertEqual(response.data, {
                         'token': token, 'username': 'wp1234', 'email': 'wp1234@yahoo.com'})

    def test_login(self):
        url = '/auth/login/'
        sample_data = {'username': 'wp1234',
                        'password': 'Qw123456Qw', 'email': 'wp1234@yahoo.com'}

        data_sample1 = {'username': 'wp12344',
                        'password': 'Qw123456Qw'}
        data_sample2 = {'username': 'wp1234',
                        'password': 'Qw123456Qww'}
        data_sample3 = {'username': 'wp12344',
                        'password': 'Qw123456Qww'}
        data_sample4 = {'username': 'wp1234',
                        'password': 'Qw123456Qw'}
        data_sample5 = {'username': 'wp12345@yahoo.com',
                        'password': 'Qw123456Qw'}
        data_sample6 = {'username': 'wp1234@yahoo.com',
                        'password': 'Qw123456Qw'}

        respons=self.client.post('/auth/create/',sample_data,format='json')
        token = respons.data.get('token')
        wrong_response_data = {"non_field_errors": [
            "Unable to log in with provided credentials."]}

        respons1 = self.client.post(url, data_sample1, format='json')
        self.assertEqual(respons1.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respons1.data,wrong_response_data)
        respons2 = self.client.post(url, data_sample1, format='json')
        self.assertEqual(respons2.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respons2.data,wrong_response_data)
        respons3 = self.client.post(url, data_sample1, format='json')
        self.assertEqual(respons3.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respons3.data,wrong_response_data)
        respons4 = self.client.post(url, data_sample4, format='json')
        self.assertEqual(respons4.status_code,status.HTTP_200_OK)
        self.assertEqual(respons4.data,{'token':token})
        respons5 = self.client.post(url, data_sample5, format='json')
        self.assertEqual(respons3.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(respons3.data,wrong_response_data)
        respons6 = self.client.post(url, data_sample6, format='json')
        self.assertEqual(respons4.status_code,status.HTTP_200_OK)
        self.assertEqual(respons4.data,{'token':token})


class CityTestCase(APITestCase):
    def setUp(self):
        City.objects.create(name='تهران')
        City.objects.create(name='شیراز')
        City.objects.create(name='اصفهان')

    def test_get_url(self):
        url1 = '/auth/cities/'
        url2 = '/auth/all-cities/'
        response1 = self.client.get(url1, format='json')
        response2 = self.client.get(url2, format='json')
        response3 = self.client.post(url2, format='json')
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_duplicate(self):
        with self.assertRaises(IntegrityError):
            City.objects.create(name='تهران')

    def test_db(self):
        qs1 = City.objects.all()
        self.assertEqual(qs1.count(), 3)
        qs2 = City.objects.filter(name='شیراز')
        self.assertTrue(qs2.exists())
        qs3 = City.objects.filter(name='رشت')
        self.assertFalse(qs3.exists())

    def test_get_method(self):
        url = '/auth/all-cities/'
        response = self.client.get(url)
        data = [{'id': 1, 'name': 'تهران'}, {
            'id': 2, 'name': 'شیراز'}, {'id': 3, 'name': 'اصفهان'}]
        self.assertEqual(response.data, data)
