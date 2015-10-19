from django.conf.urls import include, url
from django.contrib import admin
from clavutich.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
