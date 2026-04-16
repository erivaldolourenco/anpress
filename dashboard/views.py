from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

from blog.models import Post
from pages.models import Page

from .forms import (
    DashboardUserCreateForm,
    DashboardUserUpdateForm,
    PageForm,
    PostForm,
)


User = get_user_model()


class DashboardLoginView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True


class DashboardLogoutView(LogoutView):
    next_page = reverse_lazy('dashboard:login')


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = Post.objects.count()
        context['published_post_count'] = Post.objects.filter(status=Post.Status.PUBLISHED).count()
        context['page_count'] = Page.objects.count()
        context['published_page_count'] = Page.objects.filter(status=Page.Status.PUBLISHED).count()
        context['user_count'] = User.objects.count()
        context['recent_posts'] = Post.objects.select_related('author')[:5]
        return context


class DashboardListMixin(LoginRequiredMixin):
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(summary__icontains=search) | Q(content__icontains=search)
            )
        if status in {'draft', 'published'}:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        context['status_filter'] = self.request.GET.get('status', '').strip()
        return context


class PostListView(DashboardListMixin, PermissionRequiredMixin, ListView):
    permission_required = 'blog.view_post'
    template_name = 'dashboard/post_list.html'
    model = Post
    context_object_name = 'posts'


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_post'
    template_name = 'dashboard/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('dashboard:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post criado com sucesso.')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_post'
    template_name = 'dashboard/post_form.html'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('dashboard:post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Post atualizado com sucesso.')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_post'
    model = Post
    template_name = 'dashboard/post_confirm_delete.html'
    success_url = reverse_lazy('dashboard:post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Post removido com sucesso.')
        return super().form_valid(form)


class PageListView(DashboardListMixin, PermissionRequiredMixin, ListView):
    permission_required = 'pages.view_page'
    template_name = 'dashboard/page_list.html'
    model = Page
    context_object_name = 'pages'


class PageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'pages.add_page'
    template_name = 'dashboard/page_form.html'
    form_class = PageForm
    success_url = reverse_lazy('dashboard:page_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Página criada com sucesso.')
        return super().form_valid(form)


class PageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'pages.change_page'
    template_name = 'dashboard/page_form.html'
    model = Page
    form_class = PageForm
    success_url = reverse_lazy('dashboard:page_list')

    def form_valid(self, form):
        messages.success(self.request, 'Página atualizada com sucesso.')
        return super().form_valid(form)


class PageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'pages.delete_page'
    model = Page
    template_name = 'dashboard/page_confirm_delete.html'
    success_url = reverse_lazy('dashboard:page_list')

    def form_valid(self, form):
        messages.success(self.request, 'Página removida com sucesso.')
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_user'
    template_name = 'dashboard/user_list.html'
    model = User
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.prefetch_related('groups').order_by('username')
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(username__icontains=q)
                | Q(email__icontains=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        return context


class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'auth.add_user'
    template_name = 'dashboard/user_form.html'
    form_class = DashboardUserCreateForm
    success_url = reverse_lazy('dashboard:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário criado com sucesso.')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'
    template_name = 'dashboard/user_form.html'
    form_class = DashboardUserUpdateForm
    model = User
    success_url = reverse_lazy('dashboard:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Usuário atualizado com sucesso.')
        return super().form_valid(form)


class MediaListView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/media_list.html'
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.avif'}
    audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'}
    video_extensions = {'.mp4', '.webm', '.mov', '.mkv', '.avi'}
    document_extensions = {'.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.csv'}

    def _detect_type(self, suffix: str) -> str:
        if suffix in self.image_extensions:
            return 'image'
        if suffix in self.audio_extensions:
            return 'audio'
        if suffix in self.video_extensions:
            return 'video'
        if suffix in self.document_extensions:
            return 'document'
        return 'other'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media_root = Path(settings.MEDIA_ROOT)
        media_items = []
        q = self.request.GET.get('q', '').strip().lower()
        media_type = self.request.GET.get('tipo', 'all').strip()
        date_filter = self.request.GET.get('data', 'all').strip()

        if media_root.exists():
            for file_path in media_root.rglob('*'):
                if not file_path.is_file():
                    continue
                suffix = file_path.suffix.lower()
                file_type = self._detect_type(suffix)
                file_name = file_path.name

                if q and q not in file_name.lower():
                    continue
                if media_type != 'all' and media_type != file_type:
                    continue

                rel_path = file_path.relative_to(media_root).as_posix()
                encoded_path = quote(rel_path, safe='/')
                media_url = f"{settings.MEDIA_URL}{encoded_path}"
                modified_at = datetime.fromtimestamp(
                    file_path.stat().st_mtime,
                    tz=timezone.get_current_timezone(),
                )

                now = timezone.now()
                if date_filter == 'today' and modified_at.date() != now.date():
                    continue
                if date_filter == '7d' and modified_at < now - timedelta(days=7):
                    continue
                if date_filter == '30d' and modified_at < now - timedelta(days=30):
                    continue
                if date_filter == 'year' and modified_at.year != now.year:
                    continue

                media_items.append(
                    {
                        'name': file_name,
                        'url': media_url,
                        'path': rel_path,
                        'type': file_type,
                        'is_image': file_type == 'image',
                        'modified_at': modified_at,
                    }
                )

        context['media_items'] = sorted(media_items, key=lambda item: item['name'].lower())
        context['q'] = self.request.GET.get('q', '').strip()
        context['tipo'] = media_type
        context['data'] = date_filter
        return context
