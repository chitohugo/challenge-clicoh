import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import User, Product, Order, OrderDetail


class OrderTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user = User(
            email='test@test.com',
            first_name='Testing',
            last_name='Testing',
            username='testing'
        )
        cls.user.set_password('test123')
        cls.user.save()

        response = cls.client.post(
            '/api/v1/token/', {
                'username': 'testing',
                'password': 'test123',
            },
            format='json'
        )
        result = json.loads(response.content)
        cls.access_token = result['access']

        cls.product = Product(
            name="Cerveza",
            price="180",
            stock=1000,
            user_id=str(cls.user)
        )
        cls.product.save()

        cls.order = Order(
            user_id=str(cls.user)
        )
        cls.order.save()

        cls.order_detail = OrderDetail(
            quantity=20,
            order_id=str(cls.order),
            product_id=str(cls.product)
        )
        cls.order_detail.save()

    def test_create_order(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        payload = {
            "order_details": [{
                "quantity": "10",
                "product_id": str(self.product)
            }
            ]
        }

        response = self.client.post(
            f'/api/v1/order',
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order_detail = OrderDetail.objects.get(order_id=response.data['id'])
        self.assertEqual(
            str(order_detail.product_id),
            payload['order_details'][0]['product_id'],
        )

    def test_list_order(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = self.client.get(
            f'/api/v1/order',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_order(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        id = str(self.order)
        response = self.client.get(
            f'/api/v1/order/{id}',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_order(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        id = str(self.order)
        response = self.client.delete(
            f'/api/v1/order/{id}',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_order(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        payload = {
            "order_details": [{
                "quantity": "10",
                "product_id": str(self.product)
            }
            ]
        }

        response = self.client.post(
            f'/api/v1/order',
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload['quantity'] = 50

        id = str(self.order)
        response = self.client.put(
            f'/api/v1/order/{id}',
            payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
