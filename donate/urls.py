from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns

from donate.payments import urls as payments_urls

# Private URLs are not meant to be cached.
private_urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', include(payments_urls)),
]


# Public URLs that are meant to be cached.
urlpatterns = [
    path('sitemap.xml', sitemap),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # Add views for testing 404 and 500 templates
        path('test404/', TemplateView.as_view(template_name='patterns/pages/wagtail/404.html')),
        path('test500/', TemplateView.as_view(template_name='patterns/pages/wagtail/500.html')),
    ]

    # Try to install the django debug toolbar, if exists
    if apps.is_installed('debug_toolbar'):
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Set vary header to instruct cache to serve different version on different
# cookies, different request method (e.g. AJAX) and different protocol
# (http vs https).
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers('Cookie', 'X-Requested-With', 'X-Forwarded-Proto',
                    'Accept-Encoding')
)

# Join private and public URLs.
urlpatterns = private_urlpatterns + urlpatterns + [
    # Add Wagtail URLs at the end.
    # Wagtail cache-control is set on the page models's serve methods.
    path('', include(wagtail_urls)),
]
