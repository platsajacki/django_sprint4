from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User
from .models import Post, Category, Profile
from .forms import PostForm


class PostMixin:
    model = Post


class IndexListView(PostMixin, ListView):
    queryset = Post.published.all()
    paginate_by = 10


class PostDetailView(PostMixin, DetailView):
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(
            Post.published.all(),
            pk=kwargs['pk']
        )
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


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
        paginator = Paginator(context['post_list'], 10)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.get_page(1)
        context['page_obj'] = page_obj
        return context


class ProfileMixin:
    model = Profile


class ProfileListView(LoginRequiredMixin, ProfileMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['profile'] = get_object_or_404(User.objects, username=username)
        context['post_list'] = (
            Post.published
            .filter(author_id__username=username).all()
        )
        paginator = Paginator(context['post_list'], 10)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            page_obj = paginator.get_page(1)
        context['page_obj'] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, ProfileMixin, UpdateView):
    pass
