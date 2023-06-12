from django.db import models
from django.urls import reverse
from .managers import PostManager
from users.models import User
from core.models import PublishedModel

SLUG_HELP_TXT = ('Идентификатор страницы для URL; разрешены символы латиницы, '
                 'цифры, дефис и подчёркивание.')
PUB_DATE_HELP_TXT = ('Если установить дату и время в будущем — '
                     'можно делать отложенные публикации.')


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
        null=True, blank=True,
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

    objects = models.Manager()
    published = PostManager()

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Profile(models.Model):
    image = models.ImageField(
        verbose_name='Фото',
        null=True, blank=True,
        upload_to='profile'
    )
    author = models.OneToOneField(
        User, verbose_name='Блоггер',
        on_delete=models.CASCADE
    )
    bio = models.TextField(
        verbose_name='Биография',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'Профиль'

    def __str__(self):
        return str(self.author.username)
