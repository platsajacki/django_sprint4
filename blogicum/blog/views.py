from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Profile
from .forms import PostForm


class PostMixin:
    model = Post


class PaginatorMixin:
    paginate_by = 10


class IndexListView(PostMixin, PaginatorMixin, ListView):
    queryset = Post.published.all()


class PostDetailView(PostMixin, DetailView):
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Post.published.all(),
            pk=kwargs['pk']
        )
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm


class CategoryListView(ListView):
    model = Category

    def dispatch(self, request, *args, **kwargs):
        self.post_list = get_list_or_404(
            Post.published.all(),
            category__slug=kwargs['category_slug']
        )
        self.category = get_object_or_404(
            Category.objects
            .values('title', 'description'),
            slug=kwargs['category_slug'],
            is_published=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = self.post_list
        context['category'] = self.category
        return context


class ProfileMixin:
    model = Profile


class ProfileListView(ProfileMixin, PaginatorMixin, ListView):
    pass
