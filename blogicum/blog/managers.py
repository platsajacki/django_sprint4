from django.db import models
from django.utils import timezone as tz


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lt=tz.now(),
            category__is_published=True
        )

    def related_table(self):
        return self.select_related('author', 'location', 'category')


class PostManager(models.Manager):
    def get_queryset(self):
        return (
            PostQuerySet(self.model)
            .related_table()
            .published()
        )


class CommentQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def related_table(self):
        return (
            self.select_related('author', 'post')
        )


class CommentManager(models.Manager):
    def get_queryset(self):
        return (
            CommentQuerySet(self.model)
            .related_table()
            .published()
        )
