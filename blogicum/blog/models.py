from django.db import models
from django.utils import timezone as tz
from django.contrib.auth import get_user_model
from core.models import PublishedModel

SLUG_HELP_TXT = ('Идентификатор страницы для URL; разрешены символы латиницы, '
                 'цифры, дефис и подчёркивание.')
PUB_DATE_HELP_TXT = ('Если установить дату и время в будущем — '
                     'можно делать отложенные публикации.')

User = get_user_model()


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


class Category(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=SLUG_HELP_TXT
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedModel):
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=PUB_DATE_HELP_TXT
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )

    objects = models.Manager()
    published = PostManager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
