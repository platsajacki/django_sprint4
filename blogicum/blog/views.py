from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from blog.models import Post, Category


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
