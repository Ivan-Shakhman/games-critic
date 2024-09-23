from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL, Avg
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(AbstractUser):
    pseudonym = models.CharField(max_length=100, null=True, blank=True)
    favorite_games = models.ManyToManyField(
        "Game",
        related_name="favorite_by",
        blank=True,
    )

    class Meta:
        verbose_name = "author"
        verbose_name_plural = "authors"
        ordering = ["username"]

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})

    def average_rating(self):
        avg_rating = self.review_set.aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            return round(avg_rating, 1)
        return 0
    def __str__(self):
        return f"{self.username}"


class Game(models.Model):
    name = models.CharField(max_length=255)
    image = CloudinaryField('image')
    description = models.TextField()
    price = models.DecimalField(max_digits=4, decimal_places=2)
    genre = models.ForeignKey(
        Genre,
        on_delete=SET_NULL,
        related_name="games",
        null=True
    )
    authors = models.ManyToManyField(Author, related_name="games")
    release_date = models.DateField()

    def average_rating(self):
        reviews = self.reviews.all()
        average = reviews.aggregate(Avg("rating"))["rating__avg"]
        return round(average, 1) if average else "N/A"

    def __str__(self):
        return f"{self.name} genre: {self.genre}"


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

    def short_content(self):
        return self.content[:60] + "..." if len(self.content) > 60 else self.content

    def __str__(self):
        return f"({self.author.pseudonym}) {self.title}"




