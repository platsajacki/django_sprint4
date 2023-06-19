from django.db import models
from django.db.models import Count
from django.utils import timezone as tz


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lt=tz.now(),
            category__is_published=True
        )

    def count_comment(self):
        return self.annotate(comment_count=Count('comment'))

    def related_table(self):
        return self.select_related('author', 'location', 'category')


class PostManager(models.Manager):
    def get_queryset(self):
        return (
            PostQuerySet(self.model)
            .published()
            .count_comment()
            .order_by('-pub_date')
        )


class CommentQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def related_table(self):
        return self.select_related('author')


class CommentManager(models.Manager):
    def get_queryset(self):
        return (
            CommentQuerySet(self.model)
            .related_table()
            .published()
        )
