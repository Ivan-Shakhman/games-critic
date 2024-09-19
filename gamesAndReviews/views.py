from django.shortcuts import render

from gamesAndReviews.models import Author, Game, Review, Genre


def index(request):
    """View function for the home page of the site."""

    num_authors = Author.objects.count()
    num_games = Game.objects.count()
    num_reviews = Review.objects.count()
    num_genres = Genre.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_authors": num_authors,
        "num_games": num_games,
        "num_reviews": num_reviews,
        "num_genres": num_genres,
        "num_visits": num_visits + 1,
    }

    return render(request, "gamesAndReviews/index.html", context=context)
