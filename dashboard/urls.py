from django.urls import path

from .views import (
    DashboardHomeView,
    DashboardLoginView,
    DashboardLogoutView,
    MediaListView,
    PageCreateView,
    PageDeleteView,
    PageListView,
    PageUpdateView,
    PostCreateView,
    PostDeleteView,
    PostListView,
    PostUpdateView,
    UserCreateView,
    UserListView,
    UserUpdateView,
)

app_name = 'dashboard'

urlpatterns = [
    path('login/', DashboardLoginView.as_view(), name='login'),
    path('logout/', DashboardLogoutView.as_view(), name='logout'),
    path('', DashboardHomeView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/novo/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/editar/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/excluir/', PostDeleteView.as_view(), name='post_delete'),
    path('paginas/', PageListView.as_view(), name='page_list'),
    path('paginas/nova/', PageCreateView.as_view(), name='page_create'),
    path('paginas/<int:pk>/editar/', PageUpdateView.as_view(), name='page_update'),
    path('paginas/<int:pk>/excluir/', PageDeleteView.as_view(), name='page_delete'),
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/novo/', UserCreateView.as_view(), name='user_create'),
    path('usuarios/<int:pk>/editar/', UserUpdateView.as_view(), name='user_update'),
    path('midia/', MediaListView.as_view(), name='media_list'),
]
