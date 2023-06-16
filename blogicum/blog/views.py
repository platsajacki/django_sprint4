from django.shortcuts import get_object_or_404, get_list_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone as tz
from django.core.exceptions import PermissionDenied
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Category, User
from .forms import ProfileForm
from constants import POST_PER_PAGE
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import (
    PostMixin, CommentDataMixin, PostFormMixin, PostDispatchMixin,
    PaginatorMixin, ProfileMixin, CommentMixin, CommentObjectMixin,
    CommentDispatchMixin, PostUrlMixin
)


class IndexListView(PostMixin, ListView):
    queryset = Post.posts.published()
    paginate_by = POST_PER_PAGE


class PostDetailView(PostMixin, CommentDataMixin, DetailView):
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post.posts.all(),
            pk=kwargs['pk']
        )
        if instance.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        elif instance.is_published:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostCreateView(LoginRequiredMixin, PostFormMixin,
                     PostMixin, PostUrlMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostFormMixin, PostMixin,
                     PostUrlMixin, UpdateView):
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Post.posts.all_posts(),
            pk=kwargs['pk']
        )
        if instance.author != request.user:
            return redirect('blog:post_detail', self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, PostDispatchMixin,
                     PostMixin, DeleteView):
    success_url = reverse_lazy('blog:index')


class CategoryListView(ListView, PaginatorMixin):
    model = Category

    def dispatch(self, request, *args, **kwargs):
        self.post_list = get_list_or_404(
            Post.posts.published(),
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


class ProfileListView(ProfileMixin, ListView, PaginatorMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['profile'] = get_object_or_404(
            User.objects,
            username=username
        )
        post_list = (
            Post.posts.all_posts()
            .filter(author_id__username=username).all()
        )
        if str(self.request.user) != username:
            context['post_list'] = (
                post_list.filter(pub_date__lt=tz.now())
            )
            return self.setup_pagination(context)
        context['post_list'] = post_list
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


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = (
            get_object_or_404(User, username=self.request.user)
        )
        form.instance.post = (
            get_object_or_404(Post.posts.all_posts(), pk=self.kwargs['pk'])
        )
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentObjectMixin,
                        CommentDispatchMixin, CommentMixin, UpdateView):
    ...


class CommentDeleteView(LoginRequiredMixin, CommentDispatchMixin,
                        CommentObjectMixin, CommentMixin, DeleteView):
    template_name = 'blog/comment_form.html'
