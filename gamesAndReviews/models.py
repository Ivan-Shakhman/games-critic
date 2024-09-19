from django.contrib.auth.models import AbstractUser
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