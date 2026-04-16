from django.views.generic import DetailView

from core.theme import themed_template

from .models import Page


class PageDetailView(DetailView):
    model = Page
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        return [themed_template('page_detail.html')]

    def get_queryset(self):
        return Page.objects.filter(status=Page.Status.PUBLISHED).select_related('author')
