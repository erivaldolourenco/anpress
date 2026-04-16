from pages.models import Page
from .models import SiteSetting


def site_context(request):
    setting = SiteSetting.get_solo()
    menu_pages = Page.objects.filter(status=Page.Status.PUBLISHED, show_in_menu=True).order_by('title')
    return {
        'site_setting': setting,
        'menu_pages': menu_pages,
        'active_theme': setting.active_theme,
    }
