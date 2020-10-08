from model_bakery import baker
from rest_framework.test import APITestCase
from goods.models import SaleInfo
from order.models import Order, OrderDetail


class OrderTest(APITestCase):
    def setUp(self) -> None:
        self.user = baker.make('members.User', )
        self.sale_ins = SaleInfo.objects.create(discount_rate=10)
        self.goods = baker.make('goods.Goods', _quantity=10, sales=self.sale_ins, price=10000)
        self.address = baker.make('members.UserAddress', user=self.user, receiving_place='etc')
        self.order = baker.make('order.Order', user=self.user)

        self.cartItems = []
        for goods in self.goods:
            item = baker.make('carts.CartItem', goods=goods, cart=self.user.cart, status='c', order=self.order)
            self.cartItems.append(item)
        self.orderDetail = baker.make('order.OrderDetail', order=self.order)

    def test_list(self):
        qs = Order.objects.filter(user=self.user)
        response = self.client.get(f'/api/users/{self.user.id}/orders')
        self.assertEqual(200, response.status_code)

        for qs_data, res_data in zip(qs, response.data):
            self.assertEqual(qs_data.id, res_data['id'])

    def test_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "items": [self.goods[0].id, self.goods[1].id, self.goods[2].id],
        }
        response = self.client.post('/api/order', data=data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data['items'], data['items'])

    def test_detail_create(self):
        test_order = baker.make('order.Order')
        self.client.force_authenticate(user=self.user)

        data = {
            "consumer": f"{test_order.user.username[:9]}",
            "receiver": "test receiver",
            "receiver_phone": "1112223333",
            "delivery_type": "샛별배송",
            "zip_code": "12345",
            "address": "구갈동",
            "receiving_place": "문 앞",
            "entrance_password": "1234",
            "message": False,
            "order": f"{test_order.id}"
        }

        response = self.client.post(f'/api/order/{test_order.id}/detail', data=data)
        self.assertEqual(201, response.status_code)
        qs = OrderDetail.objects.last()
        self.assertEqual(response.data['order'], qs.order.id)

    def test_order_destroy(self):
        response = self.client.delete(f'/api/order/{self.order.id}')
        self.assertEqual(401, response.status_code)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/order/{self.order.id}')
        self.assertEqual(204, response.status_code)

    # def test_payment(self):
        # self.client.force_authenticate(user=self.user)
        # response = self.client.post(f'/api/order/{self.order.id}/payment')
        # self.fail()

    def test_order_detail(self):
        self.client.force_authenticate(user=self.user)
        self.order2 = baker.make('order.Order', user=self.user)
        data = {
            "consumer": "jyh",
            "receiver": "receiver",
            "receiver_phone": "12334567",
            "delivery_type": "샛별배송",
            "zip_code": "3456-123",
            "address": "test",
            "receiving_place": "문 앞",
            "message": "직후",
            "payment_type": "카카오페이",
            "order": f'{self.order.id}'
        }
        response = self.client.post(f'/api/order/{self.order2.id}/detail', data=data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(data['consumer'], response.data['consumer'])
