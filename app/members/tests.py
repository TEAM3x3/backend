from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery import baker
from munch import Munch
from rest_framework import status
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
            self.assertEqual(user_response['name'], user.name)

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
        print(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.username, data['username'])

    def test_retrieve(self):
        test_user = self.users[0]
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/api/users/{self.users[0].pk}')
        print(response)
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
        self.assertNotEquals(user_response.user, prev_username)

        self.fail()
