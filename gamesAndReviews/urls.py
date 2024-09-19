from django.conf.urls.static import static
from django.urls import path

from GamesCritic import settings
from gamesAndReviews.views import index

urlpatterns = [
    path("", index),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name="games_and_reviews"