from django.db import models

PUBLISHED_HELP_TXT = 'Снимите галочку, чтобы скрыть публикацию.'


class PublishedModel(models.Model):
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано',
                                       help_text=PUBLISHED_HELP_TXT)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
