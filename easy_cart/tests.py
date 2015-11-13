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


class TestCatalog(TestCase):
    _product = u'Invertec v145s бокс с аксессуарами (кабель, маска, молоток, щетка) (lincoln electric)'
    # _category = u'Комплектные импортные сварочные полуавтоматы с отдельно подающим механизмом подачи проволоки'
    _category = u'Category'

    def setUp(self):
        try:
            self.id += 1
        except:
            self.id = 1

        self.client = Client()
        self.category = self.get_category()
        self.product = self.get_product()

    def next_id(self):
        self.id += 1
        return self.id

    def get_product(self, meta_title=False):
        title_product = '%s %d' % (self._product, self.next_id())
        product = Product(title=title_product, category=self.category, slug=slug(title_product))
        product.meta_keywords = 'meta_keywords %s' % title_product
        product.meta_description = 'meta_description %s' % title_product

        if meta_title is not False:
            product.meta_title = 'meta_title %s' % title_product
        product.save()
        return product

    def get_category(self, meta_title=False, parent=False):
        title_category = '%s %d' % (self._category, self.next_id())
        category = Category(title=title_category, slug=slug(title_category))
        category.meta_keywords = 'meta_keywords %s' % title_category
        category.meta_description = 'meta_description %s' % title_category

        if parent is not False:
            category.parent = parent

        if meta_title is not False:
            category.meta_title = 'meta_title %s' % title_category
        category.save()
        return category

    def test_meta_product_tags(self):
        product = self.product
        response = self.client.get(product.get_absolute_url())
        self.assertContains(response, "<title>%s</title>" % capfirst(product.title.lower()), html=True)
        self.assertContains(response, "<meta name='description' content='%s'>" % product.meta_description, html=True)
        self.assertContains(response, "<meta name='meta_keywords' content='%s'>" % product.meta_keywords, html=True)

        product = self.get_product(meta_title=True)
        response = self.client.get(product.get_absolute_url())
        self.assertContains(response, "<title>%s</title>" % capfirst(product.meta_title.lower()), html=True)
        self.assertContains(response, "<meta name='description' content='%s'>" % product.meta_description, html=True)
        self.assertContains(response, "<meta name='meta_keywords' content='%s'>" % product.meta_keywords, html=True)

    def test_meta_category_tags(self):
        category = self.category
        response = self.client.get(category.get_absolute_url())
        self.assertContains(response, "<title>%s</title>" % capfirst(category.title.lower()), html=True)
        self.assertContains(response, "<meta name='description' content='%s'>" % category.meta_description, html=True)
        self.assertContains(response, "<meta name='meta_keywords' content='%s'>" % category.meta_keywords, html=True)

        category = self.get_category(meta_title=True)
        response = self.client.get(category.get_absolute_url())
        self.assertContains(response, "<title>%s</title>" % capfirst(category.meta_title.lower()), html=True)
        self.assertContains(response, "<meta name='description' content='%s'>" % category.meta_description, html=True)
        self.assertContains(response, "<meta name='meta_keywords' content='%s'>" % category.meta_keywords, html=True)

    def test_content_page_product(self):
        response = self.client.get(self.product.get_absolute_url())
        product_title = capfirst(self.product.title.lower())
        self.assertContains(response, "<title>%s</title>" % product_title, html=True)
        options = {'size': (200, 200), 'crop': True}
        thumb = get_thumbnailer(self.product.image).get_thumbnail(options).url
        self.assertTemplateUsed(response, template_name='catalog/product_detail.html')
        self.assertContains(response, u'''
        <div class="col-md-9" ng-controller="Product" ng-cloak>
            <h1>%s</h1>
            <div id="alerts">
                <alert ng-repeat="alert in alerts" type="{{alert.type}}" close="closeAlert($index)">{{alert.msg}}</alert>
            </div>
            <div class="row">
                <div class="col-sm-3">
                    <div class="row text-center">
                        <div class="col-xs-12">
                            <a id="main" href="%s" class="pull-left highslide"
                                onclick="return hs.expand(this, { slideshowGroup: 1, thumbnailId: 'main' } )">
                                <img src="%s" class="img-responsive img-rounded" alt="%s" title="%s">
                            </a>
                        </div>
                        <div class="col-xs-12 cart" >
                            <form method="post" novalidate="novalidate" ng-init="product.pk='%d'">
                                <input type="number" ng-model="quantity" class="form-control" aria-label="Количество">
                                <button class="btn btn-primary" id="comment_form" type="button" ng-disabled="disabled" ng-click="add_to_cart()">
                                    В корзину
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
                <div class="col-sm-9">
                    <p>%s</p>
                </div>
            </div>
        </div>
        ''' % (product_title, self.product.image.url, thumb, product_title, product_title, self.product.pk, self.product.description), html=True)

    def test_content_page_category(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(200, response.status_code)
        product_title = capfirst(self.category.title.lower())
        self.assertContains(response, "<title>%s</title>" % product_title, html=True)

        # self.assertContains(response, u'''''', html=True)

    def set_list_breadcrumbs_for_product(self, object):
        str = ''
        for category in object.get_ancestors_and_self():
            str += '<li><a href="%s">%s</a></li>' %\
                   (category.get_absolute_url(), truncatechars(capfirst(category.title.lower()), 80))
        return str

    def set_list_breadcrumbs_for_category(self, object):
        str = ''
        for category in object.get_ancestors():
            str += '<li><a href="%s">%s</a></li>' %\
                   (category.get_absolute_url(), truncatechars(capfirst(category.title.lower()), 80))
        return str

    def test_breadcrumbs_for_product(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertContains(response, u'''
        <div class="col-xs-12">
            <ol class="breadcrumb">
                <li><a href="/">Главная</a></li>
                %s
                <li class="active">%s</li>
            </ol>
        </div>
        ''' % (self.set_list_breadcrumbs_for_product(self.product.category),
               truncatechars(capfirst(self.product.title.lower()), 80),), html=True)

        self.product.category = self.get_category(parent=self.get_category(parent=self.get_category(parent=self.get_category())))
        self.product.save()
        response = self.client.get(self.product.get_absolute_url())
        self.assertContains(response, u'''
        <div class="col-xs-12">
            <ol class="breadcrumb">
                <li><a href="/">Главная</a></li>
                %s
                <li class="active">%s</li>
            </ol>
        </div>
        ''' % (self.set_list_breadcrumbs_for_product(self.product.category),
               truncatechars(capfirst(self.product.title.lower()), 80),), html=True)

    def test_breadcrumbs_for_category(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertContains(response, u'''
        <ol class="breadcrumb">
            <li><a href="/">Главная</a></li>
            %s
            <li class="active">%s</li>
        </ol>
        ''' % (self.set_list_breadcrumbs_for_category(self.category),
               truncatechars(capfirst(self.category.title.lower()), 80), ), html=True)

        self.category.parent = self.get_category(parent=self.get_category(parent=self.get_category(parent=self.get_category())))
        self.category.save()
        response = self.client.get(self.category.get_absolute_url())
        self.assertContains(response, u'''
        <ol class="breadcrumb">
            <li><a href="/">Главная</a></li>
            %s
            <li class="active">%s</li>
        </ol>
        ''' % (self.set_list_breadcrumbs_for_category(self.category),
               truncatechars(capfirst(self.category.title.lower()), 80), ), html=True)

    def test_available_page_product(self):
        self.assertEqual(self.product.enable, True)
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.product, get_obj(self.product.slug, Product))
        self.assertEqual(self.product.category, response.context['category'])

    def test_available_page_category(self):
        self.assertEqual(self.category.enable, True)
        response = self.client.get(self.category.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.category, get_obj(self.category.slug, Category))
        self.assertEqual(self.category, response.context['category'])
        # self.assertEqual(response, response.context['page_obj'])

    # def get_category_tree_html(self, list_categories, str=''):
    #     for category in list_categories:
    #         category_title = truncatechars(capfirst(category.title.lower()), 60)
    #
    #         if category.get_children():
    #             str += u'''<a href="#cat_%d" data-toggle="collapse" class="list-group-item''' % category.pk
    #
    #             if category.slug == self.category.slug:
    #                 str += u''' list-group-item-default'''
    #
    #             str += u'''" data-parent="#cat_{}">{} <i class="fa fa-caret-down"></i></a>
    #             <div class="collapse list-group-submenu'''.format(getattr(category, 'parent.pk', ''), category_title)
    #
    #             if self.category in category.get_children():
    #                 str += u''' in'''
    #
    #             str += u'''" aria-labelledby="cat_{0}" id="cat_{0}">'''.format(category.pk)
    #             str += self.get_category_tree_html(category.get_children(), str)
    #             str += u"</div>"
    #         else:
    #             str += u'''<a href="{}" class="list-group-item'''.format(category.get_absolute_url())
    #
    #             if category.slug == self.category.slug:
    #                 str += u''' list-group-item-default'''
    #
    #             str += u'''" data-parent="#cat_{}">{}</a>'''.format(getattr(category, 'parent.pk', ''), category_title)
    #     return str
    #
    # def test_left_bar(self):
    #     self.category.parent = self.get_category()
    #     self.category.save()
    #     response = self.client.get(self.category.get_absolute_url())
    #     self.assertContains(response, u'''
    #     <div class="col-md-3">
    #         <p class="lead">Каталог</p>
    #         <nav class="navbar">
    #             <div id="None">
    #                 <div class="list-group panel">%s</div>
    #             </div>
    #         </nav>
    #     </div>
    #     ''' % self.get_category_tree_html(Category.objects.filter(parent=None, enable=1).prefetch_related('categories')), html=True)


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
