from django.test import TestCase
from catalog.models import Product, Category
from cart import Cart
import datetime
from slugify import UniqueSlugify
from django.test import Client

slug = UniqueSlugify()
slug.to_lower = True


class TestCart(TestCase):
    def setUp(self):
        self.title_category = 'category 1'
        self.category = Category(title=self.title_category, slug=slug(self.title_category))
        self.category.save()
        self.title_product = 'product 1'
        self.quantity = 1
        self.price = 0
        self.client = Client()
        self.response = self.client.get('')
        self.cart = Cart(self.response._request)

    def product(self):
        product = Product(title=self.title_product, category=self.category, slug=slug(self.title_product))
        product.save()
        return {'product': product, 'unit_price': self.price, 'quantity': self.quantity}

    def test_product_add_to_cart(self):
        product = self.product()
        self.cart.add(**product)
        item = list(Cart(self.response._request))[0]
        self.assertEqual(1, len(list(Cart(self.response._request))))
        self.assertEqual(product['product'], item.product)
        self.assertEqual(product['quantity'], item.quantity)

        self.cart.add(**product)
        item = list(Cart(self.response._request))[0]
        self.assertEqual(1, len(list(Cart(self.response._request))))
        self.assertEqual(product['product'], item.product)
        self.assertEqual(2, item.quantity)

        self.quantity = 3
        product = self.product()
        self.cart.add(**product)
        item = list(Cart(self.response._request))[1]
        self.assertEqual(2, len(list(Cart(self.response._request))))
        self.assertEqual(product['product'], item.product)
        self.assertEqual(product['quantity'], item.quantity)
