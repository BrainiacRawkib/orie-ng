from django.contrib.sitemaps import Sitemap
from .models import Product


class ProductSitemap(Sitemap):
    """Product sitemap."""

    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated
