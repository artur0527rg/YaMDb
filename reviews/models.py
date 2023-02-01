from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

def year_validator(value):
    """Валидатор для поля year, модели Title."""

    if value > timezone.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше настоящего',
            params={'value': value},
        )

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE_CHOISES = [
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin')
]


# Create your models here.
class User(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.TextField(
        choices=ROLE_CHOISES,
        default=USER,
        blank=False,
    )

    class Meta:
        ordering = ['username']

class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255
    )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.slug

class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=255
        )
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.slug

class Title(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    year = models.IntegerField(validators=[year_validator])
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ['year']

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    text = models.TextField(max_length=3000)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        ordering = ['pub_date']