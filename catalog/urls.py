from django.conf.urls import url, patterns, include
from catalog import views

urlpatterns = patterns('',
                       url(r'product/(?P<slug>[-\w]+)/(?P<product_slug>[-\w]+)/', views.ProductDetailView.as_view(), name='product'),
                       url(r'(?P<slug>[-\w]+)/', views.CategoryDetailView.as_view(), name='category'),
                       )