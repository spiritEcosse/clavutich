from django.conf.urls import include, url, patterns
from django.contrib import admin
from clavutich.views import IndexView, WriteToUsView
from django.conf.urls.static import static
from django.contrib.flatpages import views
from clavutich import settings

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include('catalog.urls', app_name='catalog', namespace='catalog')),
    url(r'^cart/', include('easy_cart.urls', app_name='easy_cart', namespace='easy_cart')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^select2/', include('django_select2.urls')),
]

urlpatterns += [
    url(r'^about-us/$', views.flatpage, {'url': '/about-us/'}, name='about'),
    url(r'^contacts/$', views.flatpage, {'url': '/contacts/'}, name='contacts'),
    url(r'^svyazatsya-s-nami/', WriteToUsView.as_view(), name='write_to_us'),
    url(r'^(?P<url>.*/)$', views.flatpage),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                           document_root=settings.STATIC_ROOT)