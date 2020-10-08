from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from carts.models import CartItem
from config import settings
from config.settings.base import ROOT_DIR
from goods.models import Goods

User = get_user_model()


class CartTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make('members.User', )
        self.goods_lst = baker.make('goods.Goods', _quantity=20)

    def test_CartList(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/cart/{self.user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_CartItemCreate(self):
        test_user = self.user

        data = {
            'goods': self.goods_lst[0].id,
            'quantity': 2,
            'cart': test_user.id
        }
        self.client.force_authenticate(user=test_user)
        response = self.client.post(f'/api/cart/{test_user.id}/item', data=data)

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data['goods'], response.data['goods'])
        self.assertEqual(data['quantity'], response.data['quantity'])

    def test_cart_item_update(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        test_goods = Goods.objects.all()
        goods1 = Goods.objects.first()

        add_cart = CartItem.objects.create(goods=goods1, cart=test_user.cart, quantity=3)
        cart_item = CartItem.objects.filter(cart=test_user.cart)[0]
        data = {
            "goods": goods1.pk,
            "quantity": 10,
            "cart": test_user.pk
        }
        item1 = CartItem.objects.first()
        response = self.client.patch(f'/api/cart/{test_user.pk}/item/{item1.pk}', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_item_delete(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        test_goods = Goods.objects.all()
        goods1 = Goods.objects.first()

        add_cart = CartItem.objects.create(goods=goods1, cart=test_user.cart, quantity=3)
        item1 = CartItem.objects.first()
        response = self.client.delete(f'/api/cart/{test_user.pk}/item/{item1.pk}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
