from django.test import TestCase
from django.test.client import Client
from products.models import ProductCategory
from django.core.management import call_command


class TestProductsSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_products_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/4/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
           response = self.client.get(f'/products/{category.pk}/')
           self.assertEqual(response.status_code, 200)


    def tearDown(self):
        call_command('sqlsequencereset', 'products', 'users', 'order', 'baskets')
