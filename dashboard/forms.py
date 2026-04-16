from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.utils.text import slugify

from blog.models import Post
from pages.models import Page


User = get_user_model()


class BaseContentFormMixin:
    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip()
        title = self.cleaned_data.get('title', '').strip()
        return slug or slugify(title)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        published_at = cleaned_data.get('published_at')
        if status == 'published' and not published_at:
            cleaned_data['published_at'] = timezone.now()
        return cleaned_data


class PostForm(BaseContentFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'summary',
            'content',
            'status',
            'published_at',
            'featured_image',
            'meta_title',
            'meta_description',
        ]
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'js-rich-editor'}),
        }


class PageForm(BaseContentFormMixin, forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title',
            'slug',
            'summary',
            'content',
            'status',
            'published_at',
            'featured_image',
            'meta_title',
            'meta_description',
            'show_in_menu',
        ]
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'js-rich-editor'}),
        }


class DashboardUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'groups']


class DashboardUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_staff',
            'groups',
            'user_permissions',
        ]
