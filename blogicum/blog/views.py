from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone as tz
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import PostForm, ProfileForm
from .mixins import (
    CommentDataMixin, CommentDispatchMixin, CommentMixin, CommentObjectMixin,
    PaginatorMixin, PostDispatchMixin, ProfileUrlMixin
)
from .models import Category, Post, User
from constants import POST_PER_PAGE


class IndexListView(ListView):
    model = Post
    queryset = Post.published.all()
    paginate_by = POST_PER_PAGE


class PostDetailView(CommentDataMixin, DetailView):
    model = Post

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post.objects.related_table().count_comment(),
            pk=kwargs['pk']
        )
        if (instance.is_published and instance.pub_date < tz.now()
                or instance.author == self.request.user):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class PostCreateView(LoginRequiredMixin, ProfileUrlMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostDispatchMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class PostDeleteView(PostDispatchMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')


class CategoryListView(ListView, PaginatorMixin):
    model = Category

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category.objects
            .values('title', 'description'),
            slug=kwargs['category_slug'],
            is_published=True
        )
        self.post_list = (
            Post.published.all()
            .filter(category__slug=kwargs['category_slug'])
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = self.post_list
        context['category'] = self.category
        return self.setup_pagination(context)


class ProfileCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


class ProfileListView(ListView, PaginatorMixin):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['profile'] = (
            self.get_queryset()
            .get(username=username)
        )
        post_list = (
            Post.objects
            .related_table()
            .count_comment()
            .order_by('-pub_date')
            .filter(author_id__username=username)
            .all()
        )
        if self.request.user.username != username:
            context['post_list'] = (
                post_list.filter(pub_date__lt=tz.now())
            )
            return self.setup_pagination(context)
        context['post_list'] = post_list
        return self.setup_pagination(context)


class ProfileUpdateView(LoginRequiredMixin, ProfileUrlMixin, UpdateView):
    model = User
    form_class = ProfileForm
    slug_field = 'username'
    slug_url_kwarg = 'username'


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = (
            get_object_or_404(User, username=self.request.user)
        )
        form.instance.post = (
            get_object_or_404(
                (Post.objects
                 .related_table()
                 .count_comment()),
                pk=self.kwargs['pk'])
        )
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentObjectMixin,
                        CommentDispatchMixin, CommentMixin, UpdateView):
    ...


class CommentDeleteView(LoginRequiredMixin, CommentDispatchMixin,
                        CommentObjectMixin, CommentMixin, DeleteView):
    template_name = 'blog/comment_form.html'
