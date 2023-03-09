from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from .validators import validate_year

User = get_user_model()


class ReviewCommentBaseModel(models.Model):
    """Абстрактная базовая модель для Review и Comment."""

    text = models.TextField(
        verbose_name="Текст комментария/отзыва",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        abstract = True
        ordering = ("-id",)


class GenreCategoryBaseModel(models.Model):
    """Абстрактная базовая модель для Genre и Category."""

    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name="Идентификатор категории",
    )

    class Meta:
        abstract = True
        ordering = ("-id",)


class Genre(GenreCategoryBaseModel):
    """Модель для жанров."""

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("-id",)

    def __str__(self):
        return f"{self.slug}"


class Category(GenreCategoryBaseModel):
    """Модель для категорий."""

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("-id",)

    def __str__(self):
        return f"{self.slug}"


class Title(models.Model):
    """Модель для произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения",
    )
    year = models.IntegerField(
        verbose_name="Год издания произведения",
        validators=[validate_year],
    )
    description = models.TextField(
        verbose_name="Описание произведения",
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Жанры произведения",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
        blank=True,
        verbose_name="Категории произведения",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ("-id",)

    def __str__(self):
        return f"{self.name}"


class Review(ReviewCommentBaseModel):
    """Модель отзыва к произведениям Title."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор произведения",
    )
    score = models.IntegerField(
        default=0,
        validators=[
            validators.MaxValueValidator(
                limit_value=10, message="Значение не должно быть больше 10"
            ),
            validators.MinValueValidator(
                limit_value=1, message="Значение не должно быть меньше 1"
            ),
        ],
        verbose_name="Оценка произведения",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_review"
            )
        ]
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.text[:settings.LENGTH_TEXT]}"


class Comment(ReviewCommentBaseModel):
    """Модель комментария к отзыву Review."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Комментарий",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        constraints = [
            models.UniqueConstraint(
                fields=("review", "author"), name="unique_comment"
            )
        ]
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.text[:settings.LENGTH_TEXT]}"
