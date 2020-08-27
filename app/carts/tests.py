from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

User = get_user_model()


class CartTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User(username='test_cartUser', password='1111')
        self.user.set_password(self.user.password)
        self.user.save()

        self.fail()

    # def test_create(self):
    #     test_user = self.user[0]
    #
    #     data = {
    #         "quantity": 1,
    #         "user":
    #     }
    #

