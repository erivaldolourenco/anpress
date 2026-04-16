from django.db.models import Q
from django.utils import timezone
from django.views.generic import DetailView, ListView

from core.models import SiteSetting
from core.theme import themed_template

from .models import Post


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'

    def get_template_names(self):
        return [themed_template('blog_list.html')]

    def get_paginate_by(self, queryset):
        return SiteSetting.get_solo().posts_per_page

    def get_queryset(self):
        queryset = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        ).select_related('author')
        search = self.request.GET.get('q', '').strip()
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(summary__icontains=search))
        return queryset


class PostDetailView(DetailView):
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_template_names(self):
        return [themed_template('post_detail.html')]

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        ).select_related('author')
