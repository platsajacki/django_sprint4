from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryListView.as_view(),
        name='category_posts'
    ),
    path(
        'create_post/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileListView.as_view(),
        name='profile'
    ),
    # path(
    #     'edit_profile/<slug:username>/',
    #     views.ProfileUpdateView.as_view(),
    #     name='edit_profile'
    # ),
]
