from django.conf.urls.static import static
from django.urls import path

from GamesCritic import settings
from gamesAndReviews.views import index, GameListView

urlpatterns = [
    path("", index),
    path("games/", GameListView.as_view(), name="games-list"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name="games_and_reviews"