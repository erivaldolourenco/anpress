from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


User = get_user_model()


class Page(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        PUBLISHED = 'published', 'Publicado'

    title = models.CharField('Título', max_length=180)
    slug = models.SlugField('Slug', max_length=200, unique=True, blank=True)
    content = models.TextField('Conteúdo')
    summary = models.TextField('Resumo', blank=True)
    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField('Data de publicação', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pages')
    featured_image = models.FileField('Imagem destacada', upload_to='pages/', blank=True, null=True)
    meta_title = models.CharField('SEO: meta title', max_length=70, blank=True)
    meta_description = models.CharField('SEO: meta description', max_length=160, blank=True)
    show_in_menu = models.BooleanField('Exibir no menu', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:page_detail', kwargs={'slug': self.slug})
