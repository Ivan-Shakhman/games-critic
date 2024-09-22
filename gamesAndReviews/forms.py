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
            raise forms.ValidationError("Username already exists. Please choose another.")
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
            "description",
            "price",
            "genre",
            "release_date",
            "authors"
        ]

class ReviewCreationForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            "title",
            "content",
            "rating",
        ]


class GameSearchForm(forms.Form):
    name =forms.CharField(
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