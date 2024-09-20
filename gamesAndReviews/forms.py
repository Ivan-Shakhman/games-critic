from django.contrib.auth.forms import UserCreationForm

from gamesAndReviews.models import Author


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Author
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

