from django.http import request
from django.test import TestCase
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
            "nickname": "test3",
            "password": "1111",
            "phone": "010-1111-1111",
            "birthday": "1994-11-15",
            "email": "test@test.com",
            "address": "test",
            "gender": "N",
        }
        response = self.client.post('/api/users', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_retrieve(self):
        test_user = self.users[0]
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/api/users/{self.users[0].id}')
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
        token = Token.objects.create(user=self.user)
        response = self.client.delete(f'/api/users/logout',
                                      HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_find_id(self):
        password = '1111'
        self.test_user = User.objects.create_user(username='test_user', email='test_user@admin.com', password=password, nickname='test_user')
        data = {
            'nickname': 'test_user',
            'email': 'test_user@admin.com'
        }
        response = self.client.get(f'/api/users/find_id', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAddressTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User(username='test_user', password='1111')
        self.user.set_password(self.user.password)
        self.user.save()

    def test_address_list(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        response = self.client.get(f'/api/users/{test_user.id}/address')

    def test_address_create1(self):
        # 배송지 주소 생성 test
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        data = {
            "address": "서울시 성동구",
            "detail_address": "드림타워",
            "status": "T",
            "user": test_user.id
        }
        response = self.client.post(f'/api/users/{test_user.id}/address', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_response = Munch(response.data)
        self.assertTrue(user_response.address)
        self.assertEqual(user_response.address, data['address'])
        # print(user_response.address, data['address'])

        data2 = {
            "address": "서울시 성동구",
            "detail_address": "드림타워",
            "status": "T",
            "user": test_user.id
        }
        response2 = self.client.post(f'/api/users/{test_user.id}/address', data=data2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(f'/api/users/{test_user.id}/address')
        self.assertNotEquals(get_response.data[0]['status'], get_response.data[1]['status'])
        self.assertEqual(get_response.data[0]['status'], 'F')
        self.assertEqual(get_response.data[1]['status'], 'T')

    def test_address_update(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)

        data1 = {
            "address": "서울시 성동구",
            "detail_address": "드림타워",
            "status": "F",
            "user": test_user.id
        }
        response = self.client.post(f'/api/users/{test_user.id}/address', data=data1)
        response2 = self.client.get(f'/api/users/{test_user.id}/address')
        address_id = response2.data[0]['id']

        data2 = {
            "address": "서울시 성동구22",
            "detail_address": "드림타워22",
            "require_message": "문 앞에 놔주세요22",
            "status": "T",
            "user": test_user.id
        }

        response3 = self.client.patch(f'/api/users/{test_user.id}/address/{address_id}', data=data2)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_address_delete(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        data = {
            "address": "서울시 성동구",
            "detail_address": "드림타워",
            "status": "T",
            "user": test_user.pk
        }
        response = self.client.post(f'/api/users/{test_user.pk}/address', data=data)
        response2 = self.client.get(f'/api/users/{test_user.pk}/address')
        address_pk = response2.data[0]['id']
        delete_response = self.client.delete(f'/api/users/{test_user.pk}/address/{address_pk}')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)


class UserSearchTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User(username='test_user', password='1111')
        self.user.set_password(self.user.password)
        self.user.save()

    def test_search_word(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        response = self.client.get(f'/api/goods/goods_search', {'word': '칼칼'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recent_word(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        response = self.client.get(f'/api/goods/goods_search', {'word': '칼칼'})

        response2 = self.client.get(f'/api/users/{test_user.id}/searchword')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data[0]['user'], test_user.id)
        self.assertEqual(response2.data[0]['keyword'], response.wsgi_request.GET['word'])


    # def test_popular_word(self):
