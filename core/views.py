from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView

from blog.models import Post
from core.theme import themed_template


class HomeView(TemplateView):
    def get_template_names(self):
        return [themed_template('home.html')]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_posts'] = Post.objects.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        ).select_related('author')[:6]
        return context


def robots_txt(request):
    content = 'User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n'
    return HttpResponse(content, content_type='text/plain')
