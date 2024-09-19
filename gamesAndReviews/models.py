from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import ManyToManyField


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(AbstractUser):
    pseudonym = models.CharField(max_length=100)

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"
        ordering = ["pseudonym"]

    def __str__(self):
        return f"{self.pseudonym} ({self.first_name} {self.last_name})"


class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    date_of_post = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    game_to_review = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    def __str__(self):
        return f"({self.author.pseudonym}) {self.title}"