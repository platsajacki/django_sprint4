from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Comment
from .forms import PostForm, ProfileForm, CommentForm
from users.models import User
from constants import POST_PER_PAGE


class PostMixin:
    model = Post


class PostFormMixin:
    form_class = PostForm


class ProfileMixin:
    model = User


class PostDispatchMixin:
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post.published,
            pk=kwargs['pk']
        )
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment,
            pk=kwargs['pk']
        )
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PaginatorMixin:
    def setup_pagination(self, context, per_page=POST_PER_PAGE):
        paginator = Paginator(context['post_list'], per_page)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.get_page(1)
        context['page_obj'] = page_obj
        return context


class IndexListView(PostMixin, ListView):
    queryset = Post.published.all()
    paginate_by = POST_PER_PAGE


class PostDetailView(PostMixin, DetailView):
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Post.published,
            pk=kwargs['pk']
        )
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, PostFormMixin,
                     PostMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostFormMixin,
                     PostMixin, UpdateView, PostDispatchMixin):
    pass


class PostDeleteView(LoginRequiredMixin, PostDispatchMixin,
                     PostMixin, DeleteView):
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')


class CategoryListView(ListView, PaginatorMixin):
    model = Category

    def dispatch(self, request, *args, **kwargs):
        self.post_list = get_list_or_404(
            Post.published,
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
        return self.setup_pagination(context)


class ProfileListView(LoginRequiredMixin, ProfileMixin,
                      ListView, PaginatorMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['profile'] = get_object_or_404(User.objects, username=username)
        context['post_list'] = (
            Post.published
            .filter(author_id__username=username).all()
        )
        return self.setup_pagination(context)


class ProfileUpdateView(LoginRequiredMixin, ProfileMixin, UpdateView):
    form_class = ProfileForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.kwargs['username']}
        )
