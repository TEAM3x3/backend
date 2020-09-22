from django.contrib.auth import get_user_model
# Create your tests here.
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework.test import APITestCase
from config.settings import dev
from goods.models import Goods, GoodsExplain, GoodsDetail, Category, Type, GoodsType, SaleInfo

User = get_user_model()


class GoodsTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='test', password='1111')
        self.ex1 = baker.make('goods.GoodsExplain', )
        baker.make('goods.GoodsDetail', _quantity=1, goods=self.ex1.goods)

        category = Category.objects.create(name='채소')
        type = Type.objects.create(name='기본채소', category=category)

        explain = GoodsExplain.objects.first()
        detail = GoodsDetail.objects.first()
        self.g1 = Goods.objects.first()
        explain.goods = self.g1
        explain.save()
        detail.goods = self.g1
        detail.save()

        self.g2 = baker.make('goods.Goods', price=1000)
        baker.make('goods.GoodsExplain', _quantity=1, goods=self.g2)
        baker.make('goods.GoodsDetail', _quantity=1, goods=self.g2)

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
        response = self.client.get('/api/goods/1')

    def test_create(self):
        image = dev.MEDIA_ROOT + '/tree.jpeg'
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

        # def test_retrieve_category(self):
        #     response = self.client.get('/api/goods/?category=채소')
        #     goods = Goods.objects.filter(category__name='채소')
        response = self.client.get(f'/api/goods/{goods_ins.pk}')
        self.assertEqual(response.data['id'], goods_ins.id)

        goods = Goods.objects.first()
        response = self.client.get(f'/api/goods/{goods.id}')
        self.assertEqual(200, response.status_code)


    def test_sale(self):
        sale_ins = SaleInfo.objects.create(discount_rate=5)
        self.g1.sales = sale_ins
        self.g1.save()

        response = self.client.get('/api/goods/sale')
        qs = Goods.objects.filter(sales__discount_rate__isnull=False)
        for res_data in response.data:
            self.assertEqual(res_data['id'], qs[0].id)
        self.assertEqual(response.status_code, 200)

    def test_sales_price_ordering(self):
        sale_ins5 = SaleInfo.objects.create(discount_rate=5)
        sale_ins10 = SaleInfo.objects.create(discount_rate=10)
        self.g2.sales = sale_ins10
        self.g2.save()
        self.g1.sales = sale_ins5
        self.g1.save()

        qs = Goods.objects.filter(sales__discount_rate__isnull=False).order_by('price')

        response = self.client.get('/api/goods/sale?ordering=price')

        for index, res_data in enumerate(response.data):
            self.assertEqual(qs[index].id, res_data['id'])
            self.assertEqual(qs[index].price, res_data['price'])