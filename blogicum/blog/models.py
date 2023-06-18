from django.contrib.auth import get_user_model
from django.db import models

from .managers import CommentManager, PostManager, PostQuerySet
from constants import PUB_DATE_HELP_TXT, SLUG_HELP_TXT
from core.models import PublishedModel

User = get_user_model()


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
    image = models.ImageField(
        verbose_name='Фото',
        blank=True,
        upload_to='post'
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

    objects = PostQuerySet().as_manager()
    published = PostManager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'


class Comment(PublishedModel):
    text = models.TextField(
        max_length=512,
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        verbose_name='Пост'
    )

    objects = models.Manager()
    published = CommentManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарий'

    def __str__(self):
        return f'Комментарий {self.author} к посту "{self.post}".'
