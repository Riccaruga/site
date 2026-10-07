from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from exhibitions.models import Exhibition
from gallery.models import Artwork


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ["core:home", "gallery:list", "core:about",
                "exhibitions:list", "core:contacts"]

    def location(self, item):
        return reverse(item)


class ArtworkSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Artwork.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
