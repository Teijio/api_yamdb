from django.contrib.auth import get_user_model
from django.core import validators
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import LENGTH_TEXT

User = get_user_model()


class ReviewBaseModel(models.Model):
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
        ordering = ["id"]


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
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$",
                message="Идентификатор содержит недопустимый символ",
            ),
        ],
    )

    class Meta:
        abstract = True
        ordering = ["id"]


class Genre(GenreCategoryBaseModel):
    """Модель для жанров."""

    def __str__(self):
        return f"{self.slug}"


class Category(GenreCategoryBaseModel):
    """Модель для категорий."""

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
    )
    description = models.TextField(
        verbose_name="Описание произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        verbose_name="Жанры произведения",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
        verbose_name="Категории произведения",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.name}"


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.genre}"


class Review(ReviewBaseModel):
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
            validators.MaxValueValidator(10),
            validators.MinValueValidator(1),
        ],
        verbose_name="Оценка произведения",
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("title", "author")
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.text[:LENGTH_TEXT]}"


class Comment(ReviewBaseModel):
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
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.text[:LENGTH_TEXT]}"
