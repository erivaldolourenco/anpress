from django.contrib import admin

from .models import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'active_theme', 'posts_per_page')

    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()
