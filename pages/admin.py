from django.contrib import admin

from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'show_in_menu', 'author', 'published_at')
    list_filter = ('status', 'show_in_menu', 'author')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}
