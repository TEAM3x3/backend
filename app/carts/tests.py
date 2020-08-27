from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase

User = get_user_model()


class CartTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='testUser', password='1111')

    def test_list(self):
        self.fail()