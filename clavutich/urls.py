from django.conf.urls import include, url, patterns
from django.contrib import admin
from clavutich.views import IndexView
from clavutich.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static
from clavutich import settings
from django.contrib.flatpages import views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include('catalog.urls', app_name='catalog', namespace='catalog')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += [
    url(r'^about-us/$', views.flatpage, {'url': '/about-us/'}, name='about'),
    url(r'^contacts/$', views.flatpage, {'url': '/contacts/'}, name='contacts'),
    url(r'^(?P<url>.*/)$', views.flatpage),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )