from wagtail.models import Page
from django.contrib.sitemaps import Sitemap

class WagtailSitemap(Sitemap):
    def items(self):
        return Page.objects.live().public()

    def location(self, obj):
        if obj.url:
            return obj.url
        return ""
