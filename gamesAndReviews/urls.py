from django.conf.urls.static import static
from django.urls import path

from GamesCritic import settings
from gamesAndReviews.views import (
    index,
    GameListView,
    AuthorListView,
    ReviewListView,
    GameDetailView,
    ReviewDetailView,
    AuthorDetailView,
    AuthorUpdateView,
    GameCreateView,
    GameUpdateView,
    CreateReviewView,
    ReviewUpdateView,
    GameDeleteView,
    AuthorDeleteView,
    ReviewDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("games/", GameListView.as_view(), name="games-list"),
    path("games/create/", GameCreateView.as_view(), name="game-create"),
    path("games/<int:pk>/", GameDetailView.as_view(), name="games-detail"),
    path(
        "games/<int:pk>/update/",
        GameUpdateView.as_view(),
        name="games-update"
    ),
    path(
        "games/<int:pk>/delete/",
        GameDeleteView.as_view(),
        name="games-delete"
    ),
    path(
        "authors/",
        AuthorListView.as_view(),
        name="authors-list"
    ),
    path(
        "authors/<int:pk>/",
        AuthorDetailView.as_view(),
        name="author-detail"
    ),
    path(
        "authors/<int:pk>/update/",
        AuthorUpdateView.as_view(),
        name="author-update"
    ),
    path(
        "authors/<int:pk>/delete/",
        AuthorDeleteView.as_view(),
        name="author-delete"
    ),
    path(
        "reviews/",
        ReviewListView.as_view(),
        name="reviews-list"
    ),
    path(
        "reviews/create/<int:pk>/",
        CreateReviewView.as_view(),
        name="review-create"
    ),
    path(
        "reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="review-detail"
    ),
    path(
        "reviews/<int:pk>/update",
        ReviewUpdateView.as_view(),
        name="review-update"
    ),
    path(
        "reviews/<int:pk>/delete",
        ReviewDeleteView.as_view(),
        name="review-delete"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "games_and_reviews"
