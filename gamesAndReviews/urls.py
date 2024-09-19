from django.urls import path

from gamesAndReviews.views import index

urlpatterns = [
    path("", index)
]

app_name="games_and_reviews"