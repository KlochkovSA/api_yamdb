from django.db import models

from users.models import User
from .validators import validate_year

SCORE_CHOICE = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10)
)


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
        blank=True
    )
    year = models.IntegerField(
        'Дата публикации',
        validators=[validate_year]
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(to='Genre', through='TitlesGenres')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class TitlesGenres(models.Model):
    genre = models.ForeignKey(
        to='Genre',
        on_delete=models.CASCADE,
        null=True,
        related_name='genre',
    )
    title = models.ForeignKey(
        to='Title',
        on_delete=models.CASCADE,
        null=True,
        related_name='titles',
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.genre


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории',
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name', 'slug')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name', 'slug')
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        'Отзыв',
        help_text='Введите текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        choices=SCORE_CHOICE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='Unique review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    text = models.TextField(
        'Комментарий',
        help_text='Введите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
