from django.contrib.auth import get_user_model
# Create your tests here.
from model_bakery import baker
from rest_framework.test import APITestCase

from goods.models import Goods, GoodsExplain, GoodsDetail, Category, Type, GoodsType

User = get_user_model()


class GoodsTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='test', password='1111')
        baker.make('goods.GoodsExplain', _quantity=1)
        baker.make('goods.GoodsDetail', _quantity=1)

        category = Category.objects.create(name='채소')
        type = Type.objects.create(name='기본채소', category=category)

        explain = GoodsExplain.objects.first()
        detail = GoodsDetail.objects.first()
        self.g1 = Goods.objects.first()
        explain.goods = self.g1
        explain.save()
        detail.goods = self.g1
        detail.save()

        GoodsType.objects.create(type=type, goods=self.g1)

    def test_list(self):
        # 타입, 속성, pk 값이 request에 담겨 오지 않는다면 빈 리스트
        response = self.client.get('/api/goods')
        self.assertEqual(0, response.data.__len__())
        self.assertEqual(response.status_code, 200)

    def test_category_goods_list(self):
        response = self.client.get('/api/goods?category=채소')
        qs = Goods.objects.filter(types__type__category__name='채소')
        for response_data in response.data:
            self.assertEqual(response_data.get('id'), qs[0].id)
            self.assertEqual(response_data.get('title'), qs[0].title)

        self.assertEqual(response.status_code, 200)

    def test_type_goods_list(self):
        response = self.client.get('/api/goods?type=기본채소')
        qs = Goods.objects.filter(types__type__name='기본채소')
        for res_data in response.data:
            self.assertEqual(res_data['id'], qs[0].id)
            self.assertEqual(res_data['title'], qs[0].title)

        self.assertEqual(response.status_code, 200)

    def test_retrieve(self):
        response = self.client.get('/api/goods/8')
        qs = Goods.objects.first()
        self.assertEqual(response.data['id'], qs.id)

    # def test_sale(self):
    #     response =