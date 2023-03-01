from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model


User = get_user_model()


class ReviewBaseModel(models.Model):
    """Абстрактная базовая модель для Review и Comment."""
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        # on_delete=models.SET_NULL,
        related_name='reviews',
        # unique=True
        # null=True
    )
    category = models.ManyToManyField(
        Category,
        # on_delete=models.SET_NULL,
        related_name='reviews',
        # unique=True
        # null=True
    )


class Review(ReviewBaseModel):
    """Модель отзыва к произведениям Title."""
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField(default=10,
                                validators=[
                                    validators.MaxValueValidator(10),
                                    validators.MinValueValidator(1)
                                ])

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(ReviewBaseModel):
    """Модель комментария к отзыву Review."""
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
