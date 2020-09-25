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
        response = self.client.get(f'/api/cart/{test_user.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_CartItemCreate(self):
        test_user = self.user
        goods = Goods.objects.first()

        data = {
            'goods': goods.id,
            'quantity': 2,
            'cart': test_user.id
        }
        self.client.force_authenticate(user=test_user)

        test_goods = Goods.objects.all()
        goods1 = Goods.objects.first()

        add_cart = CartItem.objects.create(goods=goods1, cart=test_user.cart, quantity=3)
        item1 = CartItem.objects.first()
        response = self.client.delete(f'/api/cart/{test_user.pk}/item/{item1.pk}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

