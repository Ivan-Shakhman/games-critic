from django.test import TestCase

from gamesAndReviews.models import Author, Game
from gamesAndReviews.forms import (
    RegistrationForm,
    UpdateAuthorForm,
    ReviewCreationForm,
    AddToFavoritesForm
)

class FormTests(TestCase):

    def setUp(self):
        self.user = Author.objects.create_user(
            username='testuser',
            password='password',
            email='test@example.com'
        )

    def test_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': '123password123',
            'password2': '123password123',
        }
        form = RegistrationForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'newuser')

    def test_registration_form_invalid_username(self):
        form_data = {
            'username': 'testuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_update_author_form(self):
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'pseudonym': 'Updater'
        }
        form = UpdateAuthorForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, 'updateduser')


    def test_review_creation_form_valid(self):
        game = Game.objects.create(
            name='Test Game',
            description='Test description',
            price=49.99,
            genre=None,
            release_date='2023-01-01'
        )
        form_data = {
            'title': 'Great Game',
            'content': 'This game is fantastic!',
            'rating': 9
        }
        form = ReviewCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_to_favorites_form(self):
        game = Game.objects.create(
            name='Favorite Game',
            description='A game to be favorite.',
            price=49.99,
            genre=None,
            release_date='2023-01-01'
        )
        form_data = {'game_id': game.id}
        form = AddToFavoritesForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertIn(game, self.user.favorite_games.all())