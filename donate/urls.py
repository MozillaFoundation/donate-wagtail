from django.apps import apps
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from donate.payments import urls as payments_urls

# Patterns not subject to i18n
urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
]

urlpatterns += i18n_patterns(
    # TODO we may want to version this cache, or pre-compile the catalog at build time
    # See https://django-statici18n.readthedocs.io
    path('jsi18n/', cache_page(86400)(JavaScriptCatalog.as_view()), name='javascript-catalog'),
    path('', include(payments_urls)),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # Add views for testing 404 and 500 templates
        path('test404/', TemplateView.as_view(template_name='404.html')),
        path('test500/', TemplateView.as_view(template_name='500.html')),
    ]

    # Try to install the django debug toolbar, if exists
    if apps.is_installed('debug_toolbar'):
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns


# Add Wagtail URLs at the end.
urlpatterns += i18n_patterns(
    path('', include(wagtail_urls)),
)
