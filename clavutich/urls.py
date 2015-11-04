from django.conf.urls import include, url, patterns
from django.contrib import admin
from clavutich.views import IndexView, WriteToUsView
from clavutich.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from django.contrib.flatpages import views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include('catalog.urls', app_name='catalog', namespace='catalog')),
    url(r'^cart/', include('easy_cart.urls', app_name='easy_cart', namespace='easy_cart')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += [
    url(r'^about-us/$', views.flatpage, {'url': '/about-us/'}, name='about'),
    url(r'^contacts/$', views.flatpage, {'url': '/contacts/'}, name='contacts'),
    url(r'^svyazatsya-s-nami/', WriteToUsView.as_view(), name='write_to_us'),
    url(r'^(?P<url>.*/)$', views.flatpage),
]