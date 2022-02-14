from django.db import models

from users.models import User

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
    name = models.TextField(
        verbose_name='Название произведения',
    )
    year = models.DateField(
        'Дата публикации',
    )
    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        blank=True,
        related_name='category',
        null=True,
    )


class Category(models.Model):
    name = models.TextField(
        verbose_name='Название категории',
    )
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.TextField(
        verbose_name='Название жанра',
    )
    slug = models.SlugField(unique=True)


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
    score = models.CharField(
        max_length=1,
        choices=SCORE_CHOICE,
        null=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

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
