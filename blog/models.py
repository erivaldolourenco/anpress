from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


User = get_user_model()


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        PUBLISHED = 'published', 'Publicado'

    title = models.CharField('Título', max_length=200)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    summary = models.TextField('Resumo', blank=True)
    content = models.TextField('Conteúdo')
    status = models.CharField('Status', max_length=20, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField('Data de publicação', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    featured_image = models.FileField('Imagem destacada', upload_to='posts/', blank=True, null=True)
    meta_title = models.CharField('SEO: meta title', max_length=70, blank=True)
    meta_description = models.CharField('SEO: meta description', max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
