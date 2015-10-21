from django.conf.urls import url
from catalog import views

urlpatterns = (url(r'(?P<slug>[-\w]+)/', views.CategoryDetailView.as_view(), name='category'),
               url(r'(?P<slug>[-\w]+)/(?P<product_slug>[-\w]+)/', views.ProductDetailView.as_view(), name='product'),)
