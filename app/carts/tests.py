import os
from django.contrib.auth import get_user_model
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
        self.user = User(username='test_user', password='1111', email='test_user@test.com')
        self.user.set_password(self.user.password)
        self.user.save()

        image = settings.base.MEDIA_ROOT + '/pycharm.png'

        for i in range(5):
            test_file = SimpleUploadedFile(name='test_image.jpeg', content=open(image, 'rb', ).read(),
                                           content_type="image/jpeg"
                                           )
            test_file2 = SimpleUploadedFile(name='test_image.jpeg', content=open(image, 'rb', ).read(),
                                            content_type="image/jpeg"
                                            )

            self.goods = Goods.objects.create(img=test_file, info_img=test_file2, title='상품명',
                                              short_desc='간단설명', price='555')

    # def test_cart_list(self):
    #     test_user = self.user
    #     self.client.force_authenticate(user=test_user)
    #     # goods = Goods.objects.all()
    #
    #     response = self.client.get('f/api/carts')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.fail()

    def test_cart_create(self):
        test_user = self.user
        goods = Goods.objects.first()

        data = {
            "goods": goods.pk,
            "quantity": 1,
            "user": test_user.pk,
        }

        response = self.client.post(f'/api/carts', data=data)
        self.assertEqual(response.data['quantity'], data['quantity'])

    # def test_cart_update(self):
    #     test_user = self.user
    #
    #     goods = Goods.objects.first()
    #
    #     data = {
    #         "goods": goods.pk,
    #         "quantity": 1,
    #         "user": test_user.pk,
    #     }
    #     response = self.client.post(f'/api/carts', data=data)
    #
    #     goods2 = Goods.objects.last()
    #     data2 = {
    #         "goods": goods2.pk,
    #         "quantity": 2,
    #         "user": test_user.pk,
    #     }
    #     response2 = self.client.post(f'/api/carts', data=data2)
    #
    #     total_response = self.client.get(f'/api/carts')
    #
    #
    #     self.fail()

    def test_cart_delete(self):
        test_user = self.user
        goods = Goods.objects.first()

        data = {
            "goods": goods.pk,
            "quantity": 1,
            "user": test_user.pk,
        }
        response = self.client.delete(f'/api/carts/{self.goods.pk}')

        delete_data = CartItem.objects.last()


