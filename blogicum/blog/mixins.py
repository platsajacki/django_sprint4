from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .forms import CommentForm
from .models import Comment, Post
from constants import POST_PER_PAGE


class ProfileUrlMixin:
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentMixin:
    model = Comment
    fields = ('text',)
    queryset = Comment.published

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs['pk']})


class CommentObjectMixin:
    def get_object(self):
        queryset = self.queryset.filter(pk=self.kwargs['id'])
        return super().get_object(queryset=queryset)


class CommentDataMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (
            Comment.published
            .filter(post__id=self.kwargs['pk'])
        )
        context['form'] = CommentForm()
        return context


class PostDispatchMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            (Post.objects
             .related_table()
             .count_comment()),
            pk=kwargs['pk']
        )
        if instance.author != request.user:
            return redirect('blog:post_detail', self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class CommentDispatchMixin:
    pk_url_kwarg = 'id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Comment.published,
            pk=kwargs['id']
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
