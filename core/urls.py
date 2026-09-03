from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from search import views as search_views
from django.contrib.sitemaps.views import sitemap
from core.sitemap import WagtailSitemap
import os
# from blog.views import blog_index

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "Disallow: /admin/",
        "Disallow: /django-admin/",
        "",
        "Sitemap: https://ozford.edu.au/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

@require_GET
def llms_txt(request):
    file_path = os.path.join(settings.BASE_DIR, 'llms.txt')
    with open(file_path, 'r') as f:
        content = f.read()
    return HttpResponse(content, content_type="text/plain; charset=utf-8")

sitemaps = {
    'pages': WagtailSitemap,
}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('tinymce/', include('tinymce.urls')),
    path('agents/', include('agents.urls')),
    path('', include('payments.urls')),
    path("robots.txt", robots_txt),
    path("llms.txt", llms_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    # path('news-and-events/<int:page_id>/', blog_index, name='blog_index'),
    
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
