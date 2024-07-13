from django.db import models


class BaseFieldsModel(models.Model):
    """Абстрактная модель. Добвляет общие для моеделей поля"""

    is_published = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        null=False,
        blank=False,
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
