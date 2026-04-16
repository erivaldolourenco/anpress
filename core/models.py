from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=120, default='Anpress CMS')
    site_description = models.CharField(max_length=255, blank=True)
    active_theme = models.CharField(max_length=80, default='anpress-default')
    posts_per_page = models.PositiveSmallIntegerField(default=6)

    class Meta:
        verbose_name = 'Configuração do site'
        verbose_name_plural = 'Configurações do site'

    def __str__(self):
        return 'Configurações globais do site'

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
