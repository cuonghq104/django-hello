from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from api.models import User, Order

# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='1234567')
        user2 = User.objects.create_user(username='user2', password='1234567')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)

        response = self.client.get(reverse('user-orders'))
        assert response.status_code == status.HTTP_200_OK

        orders = response.json()
        print(orders)
        self.assertTrue(all(order['user'] == user.id for order in orders))
