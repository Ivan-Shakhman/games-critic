from django.shortcuts import render
from django.views.generic import ListView

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


class GameListView(ListView):
    model = Game
    paginate_by = 8

    def get_queryset(self):
        query_set =Game.objects.all()
        name = self.request.GET.get("name")
        if name:
            query_set = query_set.filter(name__icontains=name)
        return query_set


class AuthorListView(ListView):
    model = Author
    paginate_by = 8


class ReviewListView(ListView):
    model = Review
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = context['object_list']
        for review in reviews:
            review.short_content = review.short_content()
        context['short_content'] = reviews
        return context