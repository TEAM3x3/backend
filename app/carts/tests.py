import os
from django.contrib.auth import get_user_model
from munch import Munch
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
        self.user = User(username='test_cartUser', password='1111')
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
            # print(test_file)
            self.goods = Goods.objects.create(img=test_file, info_img=test_file2, title='상품명',
                                              short_desc='간단설명', price='555')


    def test_CartList(self):
        test_user = self.user
        self.client.force_authenticate(user=test_user)
        response = self.client.get(f'/api/carts')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_CartItemCreate(self):
        test_user = self.user
        goods = Goods.objects.first()

        data = {
            'goods': goods.id,
            'quantity': 2,
            'user': test_user.id
        }
        self.client.force_authenticate(user=test_user)
        response = self.client.post(f'/api/carts', data=data)
        self.assertEqual(response.data['quantity'], data['quantity'])

    # def test_partial_update(self):
    #     test_user = self.user
    #     goods = Goods.objects.first()
    #     goods2 = Goods.objects.last()
    #
    #     data = {
    #         'goods': goods.pk,
    #         'quantity': 2,
    #         'user': test_user.pk
    #     }
    #     response = self.client.post(f'/api/carts', data=data)
    #
    #     data2 = {
    #         'goods': goods2.pk,
    #         'quantity': 2,
    #         'user': test_user.pk
    #     }
    #     response2 = self.client.post(f'/api/carts', data=data2)
