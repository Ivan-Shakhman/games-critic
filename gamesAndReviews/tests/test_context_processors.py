from django.test import TestCase
from django.http import HttpRequest
from gamesAndReviews.context_processors import global_variables
from gamesAndReviews.models import Genre, Review, Author, Game
from datetime import datetime


class GlobalVariablesTest(TestCase):
    def setUp(self):
        self.genre1 = Genre.objects.create(name="Adventure")
        self.genre2 = Genre.objects.create(name="Action")

        self.author = Author.objects.create_user(username="testuser", password="password123")
        self.game = Game.objects.create(
            name="Test Game",
            description="Test Description",
            price=39.99,
            genre=self.genre1,
            release_date="2023-01-01"
        )
        self.review1 = Review.objects.create(
            title="Review 1",
            content="Content 1",
            rating=9,
            author=self.author,
            game_to_review=self.game,
            date_of_post=datetime.now()
        )
        self.review2 = Review.objects.create(
            title="Review 2",
            content="Content 2",
            rating=8,
            author=self.author,
            game_to_review=self.game,
            date_of_post=datetime.now()
        )
        self.review3 = Review.objects.create(
            title="Review 3",
            content="Content 3",
            rating=7,
            author=self.author,
            game_to_review=self.game,
            date_of_post=datetime.now()
        )

    def test_global_variables(self):
        request = HttpRequest()
        context = global_variables(request)

        self.assertEqual(len(context['genres']), 2)
        self.assertIn(self.genre1, context['genres'])
        self.assertIn(self.genre2, context['genres'])
        self.assertEqual(len(context['last_reviews']), 3)
