from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, EmailField

from gamesAndReviews.models import Author, Game, Review


class RegistrationForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = Author
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Author.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username already exists. Please choose another."
            )
        return username


class UpdateAuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "pseudonym"
        ]


class GameCreationForm(ModelForm):
    class Meta:
        model = Game
        fields = [
            "name",
            "image",
            "description",
            "price",
            "genre",
            "release_date",
            "authors"
        ]

        widgets = {
            "release_date": forms.DateInput(attrs={"type": "date"}),
            "authors": forms.CheckboxSelectMultiple(),
        }


class ReviewCreationForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "rating",
        ]


class GameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by Name"})
    )


class ReviewSearchForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by Title"})
    )


class AuthorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class AddToFavoritesForm(forms.Form):
    game_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self):
        game = Game.objects.get(id=self.cleaned_data['game_id'])
        if self.user and game:
            if game in self.user.favorite_games.all():
                self.user.favorite_games.remove(game)
            else:
                self.user.favorite_games.add(game)
