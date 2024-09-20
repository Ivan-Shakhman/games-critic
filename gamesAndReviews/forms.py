from django.contrib.auth.forms import UserCreationForm
from django.forms import forms, ModelForm

from gamesAndReviews.models import Author


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

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
