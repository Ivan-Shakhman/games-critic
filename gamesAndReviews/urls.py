from django.conf.urls.static import static
from django.urls import path

from GamesCritic import settings
from gamesAndReviews.forms import ReviewCreationForm
from gamesAndReviews.views import index, GameListView, AuthorListView, ReviewListView, GameDetailView, ReviewDetailView, \
    AuthorDetailView, AuthorUpdateView, GameCreateView, create_review

urlpatterns = [
    path("", index, name="index"),
    path("games/", GameListView.as_view(), name="games-list"),
    path("games/create/", GameCreateView.as_view(), name="game-create"),
    path("games/<int:pk>/", GameDetailView.as_view(), name="games-detail"),
    path("authors/", AuthorListView.as_view(), name="authors-list"),
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("authors/<int:pk>/update/", AuthorUpdateView.as_view(), name="author-update"),
    path("reviews/", ReviewListView.as_view(), name="reviews-list"),
    path("reviews/create/<int:pk>/", create_review, name="review-create"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name="games_and_reviews"
