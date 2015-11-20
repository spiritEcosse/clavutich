# --coding: utf-8--

from django.test import TestCase
from catalog.models import Product, Category
from django.utils.text import capfirst
from slugify import UniqueSlugify
from django.test import Client
from catalog.views import get_obj
from easy_thumbnails.files import get_thumbnailer
from django.template.defaultfilters import truncatechars
from cart.cart import Cart

slug = UniqueSlugify()
slug.to_lower = True

import os
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8082,8090-8100,9000-9200,7041'


class TestCart(TestCase):
    def setUp(self):
        self.title_category = 'category 1'
        self.title_product = 'product 1'
        self.quantity = 1
        self.price = 0
        self.client = Client()
        self.response = self.client.get('')
        self.cart = Cart(self.response._request)

    def category(self):
        category = Category(title=self.title_category, slug=slug(self.title_category))
        category.save()
        return category

    def product(self):
        product = Product(title=self.title_product, category=self.category(), slug=slug(self.title_product))
        product.save()
        return {'product': product, 'unit_price': self.price, 'quantity': self.quantity}

    def test_product_add_to_cart(self):
        self.assertEqual(0, self.cart.get_count_products())
        product = self.product()
        self.cart.add(**product)
        self.assertEqual(1, self.cart.get_count_products())
        item = self.cart.get_product(product['product'].pk)
        self.assertEqual(product['product'], item.product)
        self.assertEqual(product['quantity'], item.quantity)

        self.cart.add(**product)
        item = self.cart.get_product(product['product'].pk)
        self.assertEqual(1, self.cart.get_count_products())
        self.assertEqual(product['product'], item.product)
        self.assertEqual(2, item.quantity)

        self.quantity = 3
        product = self.product()
        self.cart.add(**product)
        item = self.cart.get_product(product['product'].pk)
        self.assertEqual(2, self.cart.get_count_products())
        self.assertEqual(product['product'], item.product)
        self.assertEqual(product['quantity'], item.quantity)

    def test_product_update_on_cart(self):
        product = self.product()
        self.cart.add(**product)
        item = self.cart.get_product(product['product'].pk)
        self.assertEqual(product['quantity'], item.quantity)

        product['quantity'] = 3
        self.cart.update(**product)
        item = self.cart.get_product(product['product'].pk)
        self.assertEqual(product['quantity'], item.quantity)
        self.assertEqual(1, self.cart.get_count_products())

        product = self.product()
        self.cart.add(**product)
        item = self.cart.get_product(product['product'].pk)
        self.assertEqual(product['quantity'], item.quantity)

        product['quantity'] = 3
        self.cart.update(**product)
        item = self.cart.get_product(product['product'].pk)
        self.assertEqual(product['quantity'], item.quantity)
        self.assertEqual(2, self.cart.get_count_products())

    def test_clear_from_cart(self):
        product = self.product()
        self.cart.add(**product)
        self.assertEqual(1, self.cart.get_count_products())
        product = self.product()
        self.cart.add(**product)
        self.assertEqual(2, self.cart.get_count_products())
        self.cart.clear()
        self.assertEqual(0, self.cart.get_count_products())

    def test_remove_from_cart(self):
        products = []
        self.assertQuerysetEqual(self.cart.get_products(), products)
        product_1 = self.product()
        products.append(product_1['product'])
        self.cart.add(**product_1)
        item_1 = self.cart.get_product(product_1['product'].pk)
        self.assertEqual(product_1['product'], item_1.product)
        product_2 = self.product()
        products.append(product_2['product'])
        self.cart.add(**product_2)
        self.cart.remove(product_2['product'])
        self.assertNotIn(product_2['product'], self.cart.get_products())
        self.assertEqual(1, self.cart.get_count_products())
        self.cart.remove(product_1['product'])
        self.assertNotIn(product_1['product'], self.cart.get_products())


# class AdminTestCase(LiveServerTestCase):
#     def setUp(self):
#         User.objects.create_superuser(
#             username='admin',
#             password='admin',
#             email='admin@example.com')
#
#         self.selenium = webdriver.Firefox()
#         self.selenium.maximize_window()
#         super(AdminTestCase, self).setUp()
#
#     def tearDown(self):
#         self.selenium.quit()
#         super(AdminTestCase, self).tearDownClass()
#
#     def test_create_user(self):
#         """
#         Django admin create user test
#         This test will create a user in django admin and assert that
#         page is redirected to the new user change form.
#         """
#         # Open the django admin page.
#         # DjangoLiveServerTestCase provides a live server url attribute
#         # to access the base url in tests
#         self.selenium.get(
#             '%s%s' % (self.live_server_url,  "/admin/")
#         )
#
#         # Fill login information of admin
#         username = self.selenium.find_element_by_id("id_username")
#         user = 'admin'
#         username.send_keys(user)
#         password = self.selenium.find_element_by_id("id_password")
#         password.send_keys("admin")
#
#         # Locate Login button and click it
#         self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
#         self.selenium.get(
#             '%s%s' % (self.live_server_url, "/admin/auth/user/add/")
#         )
#
#         # Fill the create user form with username and password
#         self.selenium.find_element_by_id("id_username").send_keys("test")
#         self.selenium.find_element_by_id("id_password1").send_keys("test")
#         self.selenium.find_element_by_id("id_password2").send_keys("test")
#
#         # Forms can be submitted directly by calling its method submit
#         self.selenium.find_element_by_id("user_form").submit()
#         self.assertIn(u"Изменить пользователь", self.selenium.title)
#         # from django.utils.html import escape, mark_safe
#         # self.assertEqual(self.selenium.find_element_by_class_name('alert-success').text.strip(),
#         #                  u'''"пользователь "%s" был успешно добавлен. Ниже вы можете снова его отредактировать."''' %
#         #                  user)
