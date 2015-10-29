from django.conf.urls import url, patterns, include
from catalog import views

urlpatterns = patterns('',
                       url(r'^product_add_to_cart/(?P<pk>[\d]+)/$', views.ProductAddToCart.as_view(), name='add_to_cart'),
                       url(r'^product/(?P<category_slug>[-\w]+(/[\w-]+)*)/(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name='product'),
                       url(r'^(?P<slug>[\w-]+(/[\w-]+)*)/', views.CategoryDetailView.as_view(), name='category'),
                       )