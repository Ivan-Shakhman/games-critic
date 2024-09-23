from lib2to3.fixes.fix_input import context

from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from gamesAndReviews.forms import (
    RegistrationForm,
    UpdateAuthorForm,
    GameCreationForm,
    ReviewCreationForm,
    GameSearchForm,
    AuthorSearchForm,
    ReviewSearchForm,
    AddToFavoritesForm
)
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
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["game_search_form"] = GameSearchForm(
            initial={"name": name}
        )
        context["add_to_favorite_form"] = AddToFavoritesForm()
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        genre_name = self.request.GET.get("genre", None)
        name = self.request.GET.get("name", None)
        if genre_name:
            query_set = query_set.filter(genre__name__icontains=genre_name)
        if name:
            query_set = query_set.filter(name__icontains=name)
        return query_set.order_by("-release_date")

    def post(self, request, *args, **kwargs):
        form = AddToFavoritesForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
        return redirect("games_and_reviews:games-list")


class GameDetailView(DetailView):
    model = Game


class AuthorListView(ListView):
    model = Author
    paginate_by = 6

    def get_queryset(self):
        query_set = super().get_queryset()
        username = self.request.GET.get("username", None)
        if username:
            query_set = query_set.filter(username__icontains=username)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["author_search_form"] = AuthorSearchForm(
            initial={"username": username}
        )
        return context


class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author
    queryset = Author.objects.all().prefetch_related("games__authors")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UpdateAuthorForm
    success_url = reverse_lazy("games_and_reviews:index")
    queryset = get_user_model().objects.all()


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("games_and_reviews:index")


class ReviewListView(ListView):
    model = Review
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = context['object_list']
        title = self.request.GET.get("title", "")
        for review in reviews:
            review.short_content = review.short_content()
        context['short_content'] = reviews
        context["review_search_form"] = ReviewSearchForm(
            initial={"review_title": title}
        )
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        title = self.request.GET.get("title", "")
        if title:
            query_set = query_set.filter(title__icontains=title)
        return query_set.order_by("-date_of_post")


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameCreationForm
    success_url = reverse_lazy("games_and_reviews:games-list")


class GameUpdateView(LoginRequiredMixin, UpdateView):
    form_class = GameCreationForm
    model = Game
    success_url = reverse_lazy("games_and_reviews:games-list")


class GameDeleteView(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("games_and_reviews:games-list")


class ReviewDetailView(DetailView):
    model = Review


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreationForm
    template_name = 'gamesAndReviews/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        game = get_object_or_404(Game, id=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.game_to_review = game
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("games_and_reviews:reviews-list")


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ReviewCreationForm
    model = Review
    success_url = reverse_lazy("games_and_reviews:reviews-list")


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy("games_and_reviews:reviews-list")
