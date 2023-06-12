from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Post, Category


def index(request):
    post_list = Post.published.all()[0:5]
    context = {'post_list': post_list}
    template = 'blog/index.html'
    return render(request, template, context)


def post_detail(request, id):
    post = get_object_or_404(
        Post.published.all(),
        pk=id
    )
    context = {'post': post}
    template = 'blog/detail.html'
    return render(request, template, context)


def category_posts(request, category_slug):
    post_list = get_list_or_404(
        Post.published.all(),
        category__slug=category_slug
    )
    category = get_object_or_404(
        Category.objects
        .values('title', 'description'),
        slug=category_slug,
        is_published=True
    )
    context = {'post_list': post_list,
               'category': category}
    template = 'blog/category.html'
    return render(request, template, context)


def pageNotFound(request, exception):
    return render(request, 'http404.html')
