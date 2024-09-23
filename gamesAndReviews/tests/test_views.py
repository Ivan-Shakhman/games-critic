from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from gamesAndReviews.models import Author, Game, Review, Genre
from gamesAndReviews.forms import RegistrationForm, GameCreationForm, ReviewCreationForm

class AuthorViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.author = Author.objects.create_user(
            username='authoruser',
            password='password123',
            email='author@example.com'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_author_list_view(self):
        response = self.client.get(reverse('games_and_reviews:authors-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.username)

    def test_author_detail_view(self):
        response = self.client.get(reverse('games_and_reviews:author-detail', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.username)

    def test_author_update_view(self):
        response = self.client.get(reverse('games_and_reviews:author-update', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)

    def test_author_delete_view(self):
        response = self.client.get(reverse('games_and_reviews:author-delete', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)

class GameViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.genre = Genre.objects.create(name='Action')
        self.game = Game.objects.create(
            name='Test Game',
            description='Game description.',
            image="image/upload/v1727004256/mhvex77qsxbmnydgnwez.jpg",
            price=19.99,
            genre=self.genre,
            release_date='2023-01-01'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_game_list_view(self):
        response = self.client.get(reverse('games_and_reviews:games-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.game.name)

    def test_game_detail_view(self):
        response = self.client.get(reverse('games_and_reviews:games-detail', args=[self.game.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.game.name)


    def test_game_delete_view(self):
        response = self.client.post(reverse('games_and_reviews:games-delete', args=[self.game.id]))
        self.assertFalse(Game.objects.filter(id=self.game.id).exists())

class ReviewViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.genre = Genre.objects.create(name='Action')
        self.game = Game.objects.create(
            name='Test Game',
            description='Game description.',
            price=19.99,
            genre=self.genre,
            release_date='2023-01-01'
        )
        self.review = Review.objects.create(
            title='Test Review',
            content='This is a test review.',
            rating=8,
            author=self.user,
            game_to_review=self.game
        )
        self.client.login(username='testuser', password='testpassword')

    def test_review_list_view(self):
        response = self.client.get(reverse('games_and_reviews:reviews-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.title)

    def test_review_detail_view(self):
        response = self.client.get(reverse('games_and_reviews:review-detail', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.review.title)

    def test_create_review_view(self):
        response = self.client.post(reverse('games_and_reviews:review-create', args=[self.game.id]), {
            'title': 'New Review',
            'content': 'This is a new review.',
            'rating': 9
        })
        self.assertRedirects(response, reverse('games_and_reviews:reviews-list'))
        self.assertTrue(Review.objects.filter(title='New Review').exists())

    def test_update_review_view(self):
        response = self.client.post(reverse('games_and_reviews:review-update', args=[self.review.id]), {
            'title': 'Updated Review',
            'content': 'Updated content.',
            'rating': 9
        })
        self.assertRedirects(response, reverse('games_and_reviews:reviews-list'))
        self.review.refresh_from_db()
        self.assertEqual(self.review.title, 'Updated Review')

    def test_delete_review_view(self):
        response = self.client.post(reverse('games_and_reviews:review-delete', args=[self.review.id]))
        self.assertRedirects(response, reverse('games_and_reviews:reviews-list'))
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())