from django.conf.urls import include, url, patterns
from django.contrib import admin
from clavutich.views import IndexView, WriteToUsView
from django.conf.urls.static import static
from django.contrib.flatpages import views
from clavutich import settings

from django.contrib.sitemaps.views import sitemap
from clavutich.sitemaps import StaticViewSitemap
from catalog.sitemaps import CategorySitemap, ProductSitemap
from extend_flatpages.sitemaps import ExtendFlatPage
from django.views.decorators.cache import cache_page

sitemaps = {
    'static': StaticViewSitemap,
    'flat_pages': ExtendFlatPage,
    'category': CategorySitemap,
    'product': ProductSitemap,
}

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
    url(r'^sitemap\.xml$', cache_page(24*60*60)(sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                           document_root=settings.STATIC_ROOT)