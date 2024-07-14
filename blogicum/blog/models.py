from core.models import PublishedAndCreateModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class PostQuerySet(models.QuerySet):

    def with_actual_data(self):
        return self.filter(pub_date__lte=timezone.now())

    def published(self):
        return self.filter(is_published=True)

    def category_published(self):
        return self.filter(category__is_published=True)


class PublishedPostManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return (
            PostQuerySet(self.model)
            .with_actual_data()
            .published()
            .category_published()
        )

class Category(PublishedAndCreateModel):
    """
    Модель для хранения данных о категориях.
    Содержит поля:
        title (обязательное) - заголовок категории
        description (обязательное) - описание категории
        slug (обязательное, уникальное) - идентификатор (слаг) категории
        is_published (обязательное) - доступость категории
        created_at (обязательное) - дата и время добавления категории
    """

    title = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta(PublishedAndCreateModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedAndCreateModel):
    """
    Модель для хранения данных о местоположениях.
    Содержит поля:
        name (обязательное) - название локации
        is_published (обязательное) - доступность локации
        created_at (обязательное) - дата и время создания
    """

    name = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name='Название места'
    )

    class Meta(PublishedAndCreateModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedAndCreateModel):
    """
    Модель для хранения данных о постах.
    Содержит поля:
        title (обязательное) - заголовок поста
        text (обязательное) - содержимое поста
        pub_date (обязательное) - дата и время добавления поста
        author (обязательное) - ключ, автор поста
        location - ключ, местоположение
        category - ключ, категория поста
        is_published - доступность поста
        created_at - дата и время создания поста
    """

    ELEMENTS_TO_SHOW = 5

    title = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем '
            '— можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='posts',
        verbose_name='Категория'
    )

    class Meta(PublishedAndCreateModel.Meta):
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    objects = PostQuerySet.as_manager()
    published = PublishedPostManager()
