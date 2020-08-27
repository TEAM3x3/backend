from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from goods.models import Goods

User = get_user_model()


class Cart_test(APITestCase):

    def setUp(self) -> None:
        self.user = User(username='test', password='1111', email='cccc@c.com')
        self.user.set_password(self.user.password)
        self.user.save()

        self.goods = Goods.objects.all()[:3]

        print('dddd', self.goods)
        self.fail()


    def test_list(self):
        self.fail()