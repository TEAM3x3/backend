from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        # 1
        self.users = baker.make('members.User', _quantity=2)
        # 2
        self.user = User(username='test_admin', password='1111')
        self.user.set_password(self.user.password)
        self.user.save()

    def test_list(self):
        test_user = self.users[0]
        self.client.force_authenticate(user=test_user)
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for user_response, user in zip(response.data, self.users):
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)

    def test_create(self):
        data = {
            "username": "test3",
            "user_id": "test3",
            "password": "1111",
            "phone": "010-1111-1111",
            "birthday": "1994-11-15",
            "email": "test@test.com",
            "address": "test",
            "gender": "N",
            "name": "test"
        }
        response = self.client.post('/api/users', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_retrieve(self):
        test_user = self.users[0]
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/api/users/{self.users[0].pk}')
        self.assertEqual(response.data['username'], test_user.username)

    def test_partial_update(self):
        test_user = self.users[0]
        prev_username = test_user.username

        data = {'username': 'test_name'}
        self.client.force_authenticate(user=test_user)
        response = self.client.patch(f'/api/users/{test_user.id}', data=data)
        user_response = Munch(response.data)
        self.assertTrue(user_response.username)
        self.assertEqual(user_response.username, data['username'])
        self.assertNotEquals(user_response.username, prev_username)

    def test_destroy(self):
        test_user = self.users[0]
        self.client.force_authenticate(user=test_user)
        response = self.client.delete(f'/api/users/{test_user.id}')
        self.assertTrue(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=test_user.id).exists())

    def test_login(self):
        password = '1111'
        self.test_user = User(username='test_user', email='test_user@email.com', password=password)
        self.test_user.set_password(self.test_user.password)
        self.test_user.save()

        data = {
            'username': self.test_user.username,
            'password': password
        }
        response = self.client.post(f'/api/users/login', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data.get('token'))

    def test_logout(self):
        test_user = self.users[0]
        token = Token.objects.create(user=test_user)
        response = self.client.delete(f'/api/users/logout',
                                      HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())


class UserAddressTestAPI(APITestCase):
    def setUp(self) -> None:
        self.user = User(username='test_Address', password='1111')
        self.user.set_password(self.user.password)
        self.user.save()

    def test_address_create(self):
        user = self.user
        self.client.force_authenticate(user=user)

        data = {
            "address": "서울 중구",
            "detail_address": "신당동",
            "require_message": "0000",
            "status": "T",
            "user": user.id
        }

        response = self.client.post(f'/api/users/{user.id}/address', data=data)
        response2 = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response2.data['address'][0]['require_message'], data['require_message'])
        self.assertEqual(response2.data['address'][0]['address'], data['address'])

    def test_address_list(self):
        user = self.user
        self.client.force_authenticate(user=user)

        data = {
            "address": "서울 중구",
            "detail_address": "신당동",
            "require_message": "0000",
            "status": "T",
            "user": user.id
        }

        data2 = {
            "address": "강원도 강릉",
            "detail_address": "강릉동",
            "require_message": "0000",
            "status": "F",
            "user": user.id
        }

        response = self.client.post(f'/api/users/{user.id}/address', data=data)
        response2 = self.client.post(f'/api/users/{user.id}/address', data=data2)
        response3 = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response3.data['address'][0]['address'], data['address'])
        self.assertEqual(response3.data['address'][1]['address'], data2['address'])
        self.assertEqual(len(response3.data['address']), 2)

    def test_address_update(self):
        user = self.user
        self.client.force_authenticate(user=user)

        data = {
            "address": "서울 중구",
            "detail_address": "신당동",
            "require_message": "0000",
            "status": "T",
            "user": user.id
        }

        data2 = {
            "address": "강원도 강릉",
            "detail_address": "강릉동",
            "require_message": "0000",
            "status": "F",
            "user": user.id
        }

        response = self.client.post(f'/api/users/{user.id}/address', data=data)
        response2 = self.client.post(f'/api/users/{user.id}/address', data=data2)
        address_list = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(address_list.data['address'][0]['status'], data['status'])
        self.assertEqual(address_list.data['address'][0]['status'], "T")
        self.assertEqual(address_list.data['address'][1]['status'], data2['status'])
        self.assertEqual(address_list.data['address'][1]['status'], "F")

        status_patch = {
            "status": "T"
        }
        address_pk = address_list.data['address'][1]['id']

        self.client.patch(f'/api/users/{user.id}/address/{address_pk}', data=status_patch)

        patch_list = self.client.get(f'/api/users/{user.id}')

        self.assertEqual(patch_list.data['address'][0]['address'], data['address'])
        self.assertEqual(patch_list.data['address'][0]['status'], "F")
        self.assertEqual(patch_list.data['address'][1]['address'], data2['address'])
        self.assertEqual(patch_list.data['address'][1]['status'], "T")

    def test_address_delete(self):
        user = self.user
        self.client.force_authenticate(user=user)

        data = {
            "address": "서울 중구",
            "detail_address": "신당동",
            "require_message": "0000",
            "status": "T",
            "user": user.id
        }

        response = self.client.post(f'/api/users/{user.id}/address', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        address_list = self.client.get(f'/api/users/{user.id}')
        address_pk = address_list.data['address'][0]['id']

        delete_response = self.client.delete(f'/api/users/{user.id}/address/{address_pk}')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(delete_response.data)
