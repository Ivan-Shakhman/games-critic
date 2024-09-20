from django.conf.urls.static import static
from django.urls import path

from GamesCritic import settings
from gamesAndReviews.views import index, GameListView, AuthorListView, ReviewListView, GameDetailView, ReviewDetailView

urlpatterns = [
    path("", index, name="index"),
    path("games/", GameListView.as_view(), name="games-list"),
    path("games/<int:pk>/", GameDetailView.as_view(), name="games-detail"),
    path("authors/", AuthorListView.as_view(), name="authors-list"),
    path("reviews/", ReviewListView.as_view(), name="reviews-list"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name="games_and_reviews"