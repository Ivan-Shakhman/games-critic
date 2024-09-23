from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from gamesAndReviews.models import Genre, Game, Author, Review

User = get_user_model()

class AdminSiteTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='password',
            email='admin@example.com'
        )
        self.client.login(username='admin', password='password')
        self.genre = Genre.objects.create(name='Action')
        self.author = Author.objects.create_user(
            username='author1',
            password='password',
            email='author1@example.com',
            pseudonym='Auth1'
        )
        self.game = Game.objects.create(
            name='Test Game',
            description='A description of the game.',
            price=49.99,
            genre=self.genre,
            release_date='2023-01-01'
        )
        self.review = Review.objects.create(
            title='Great Game',
            content='This game is fantastic!',
            rating=9,
            author=self.author,
            game_to_review=self.game
        )

    def test_genre_admin(self):
        url = reverse('admin:gamesAndReviews_genre_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Action')

    def test_game_admin(self):
        url = reverse('admin:gamesAndReviews_game_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Game')

    def test_author_admin(self):
        url = reverse('admin:gamesAndReviews_author_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'author1')

    def test_review_admin(self):
        url = reverse('admin:gamesAndReviews_review_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Great Game')

    def test_author_field_display(self):
        url = reverse('admin:gamesAndReviews_author_change', args=[self.author.id])
        response = self.client.get(url)
        self.assertContains(response, 'Auth1')

    def test_game_average_rating(self):
        self.assertEqual(self.game.average_rating(), 9)  # нет отзывов
        Review.objects.create(
            title='Awesome!',
            content='Really enjoyed it!',
            rating=10,
            author=self.author,
            game_to_review=self.game
        )
        self.assertEqual(self.game.average_rating(), 9.5)
