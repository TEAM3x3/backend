from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

# Create your tests here.
from model_bakery import baker
from rest_framework.test import APITestCase

from config import settings
from goods.models import Goods, GoodsExplain, GoodsDetail

User = get_user_model()


class GoodsTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='test', password='1111')
        baker.make('goods.GoodsExplain', _quantity=1)
        baker.make('goods.GoodsDetail', _quantity=1)

    def test_list(self):
        response = self.client.get('/api/goods')
        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        response = self.client.get('/api/goods/1')

    def test_create(self):
        image = settings.dev.MEDIA_ROOT + '/tree.jpeg'
        test_image = SimpleUploadedFile(
            name='tree.jpeg',
            content=open(image, "rb").read(),
            content_type="image/jpeg"
        )
        test_image2 = SimpleUploadedFile(
            name='tree.jpeg',
            content=open(image, "rb").read(),
            content_type="image/jpeg"
        )

        goods_ins = Goods.objects.create(
            img=test_image,
            info_img=test_image2,
            title='testTitle',
            short_desc='short_desc',
            price=1,
        )

    def test_retrieve_category(self):
        response = self.client.get('/api/goods/?category=채소')
        goods = Goods.objects.filter(category__name='채소')

