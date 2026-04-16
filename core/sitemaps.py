from django.contrib.sitemaps import Sitemap
from django.utils import timezone

from blog.models import Post
from pages.models import Page


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED, published_at__lte=timezone.now())

    def lastmod(self, obj):
        return obj.updated_at


class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Page.objects.filter(status=Page.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at
