from django.conf.urls import include, url
from django.contrib import admin
from clavutich.views import IndexView
from clavutich.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalog/', include('catalog.urls', app_name='catalog', namespace='catalog')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
