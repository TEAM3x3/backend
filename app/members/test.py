from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from members.models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        # pip install model-bakery
        self.users = baker.make('members.User', _quantity=3)

    def test_user_list(self):
        test_user = self.users[0]
        self.client.force_authenticate(user=test_user)
        response = self.client.get('/api/users')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for user_response, user in zip(response.data, self.users):
            self.assertEqual(user_response['id'], user.id)
            self.assertEqual(user_response['username'], user.username)

    def test_user_create(self):
        data = {
            "username": "bababababa",
            "password": "1111",
            "email": "jan@nam.net",
            "phone": "01011112222",
            "gender": "F"
        }
        response = self.client.post('/api/users', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])

    def test_user_retrieve(self):
        instance = self.users[0]
        self.client.force_authenticate(user=self.users[0])
        response = self.client.get(f'/api/users/{self.users[0].pk}')

        self.assertEqual(instance.username, response.data['username'])

    def test_user_update(self):
        instance = self.users[0]
        self.client.force_authenticate(user=self.users[0])

        data = {
            "email": "uuu@uuu.net"
        }
        response = self.client.patch(f'/api/users/{self.users[0].pk}', data=data)

        self.assertEqual(response.data['email'], data['email'])
        self.assertNotEqual(instance.email, response.data['email'])

    def test_user_delete(self):
        user = self.users[0]
        self.client.force_authenticate(user=user)
        response = self.client.delete(f'/api/users/{user.pk}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(response.data)

        pk = User.objects.filter(id=user.id).count()
        self.assertEqual(pk, 0)

