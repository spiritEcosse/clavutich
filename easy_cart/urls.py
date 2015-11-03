__author__ = 'igor'
from django.conf.urls import url
from easy_cart.views import ShowView, OrderView, RemoveProduct, UpdateQuantityProductView

urlpatterns = [
    url(r'^$', ShowView.as_view(), name='show'),
    url(r'^remove/(?P<pk>[\d]+)/$', RemoveProduct.as_view(), name='remove'),
    url(r'^order/$', OrderView.as_view(), name='order'),
    # url(r'^make_order/$', SuccessMakeOrderView.as_view(), name='order'),
    url(r'^update_quantity_product/(?P<pk>[\d]+)/$', UpdateQuantityProductView.as_view(), name='update_quantity_product'),
]