from django.test import TestCase
from gamesAndReviews.models import Genre, Author, Game, Review
from django.contrib.auth.hashers import make_password


class GenreModelTest(TestCase):
    def test_string_representation(self):
        genre = Genre(name="Action")
        self.assertEqual(str(genre), genre.name)


class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            username="author_user",
            password=make_password("password"),
            email="author@example.com",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.author), "author_user")

    def test_average_rating(self):
        self.assertEqual(self.author.average_rating(), 0)


class GameModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Adventure")
        self.author = Author.objects.create(
            username="author_user",
            password=make_password("password"),
            email="author@example.com",
        )
        self.game = Game.objects.create(
            name="Game 1",
            description="A fun adventure game.",
            price=29.99,
            genre=self.genre,
            release_date="2023-01-01",
        )
        self.game.authors.add(self.author)

    def test_string_representation(self):
        self.assertEqual(str(self.game), "Game 1 genre: Adventure")

    def test_average_rating(self):
        self.assertEqual(self.game.average_rating(), "N/A")


class ReviewModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Action")
        self.author = Author.objects.create(
            username="author_user",
            password=make_password("password"),
            email="author@example.com",
        )
        self.game = Game.objects.create(
            name="Game 1",
            description="A fun adventure game.",
            price=29.99,
            genre=self.genre,
            release_date="2023-01-01",
        )
        self.review = Review.objects.create(
            title="Great game!",
            content="I loved playing this game. It was amazing!",
            rating=9,
            author=self.author,
            game_to_review=self.game,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.review), "(None) Great game!")

    def test_short_content(self):
        self.assertEqual(
            self.review.short_content(),
            "I loved playing this game. It was amazing!"
        )
