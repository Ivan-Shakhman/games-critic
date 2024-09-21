from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from gamesAndReviews.forms import RegistrationForm, UpdateAuthorForm, GameCreationForm, ReviewCreationForm
from gamesAndReviews.models import Author, Game, Review, Genre


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("games_and_reviews:index")
    else:
        form = RegistrationForm()
    return render(
        request,
        "registration/registration.html",
        {"form": form}
    )

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
        query_set =super().get_queryset()
        genre_name = self.request.GET.get("genre", None)
        if genre_name:
            query_set = query_set.filter(genre__name__icontains=genre_name)
        return query_set


class GameDetailView(DetailView):
    model = Game


class AuthorListView(ListView):
    model = Author
    paginate_by = 8


class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author
    queryset = Author.objects.all().prefetch_related("games__authors")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateAuthorForm
    success_url = reverse_lazy("games_and_reviews:index")
    queryset = get_user_model().objects.all()



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



class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameCreationForm
    success_url = reverse_lazy("games_and_reviews:games-list")


class GameUpdateView(LoginRequiredMixin, UpdateView):
    form_class = GameCreationForm
    model = Game
    success_url = reverse_lazy("games_and_reviews:games-list")


class ReviewDetailView(DetailView):
    model = Review


def create_review(request, pk):
    game = get_object_or_404(Game, id=pk)
    if request.method == 'POST':
        form = ReviewCreationForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.game_to_review = game
            review.save()
            return redirect("games_and_reviews:reviews-list")
    else:
        form = ReviewCreationForm()

    return render(request, 'gamesAndReviews/review_form.html', {'form': form, "game": game})
