from gamesAndReviews.models import Genre, Review


def global_variables(request):
    return {
        "genres": Genre.objects.all(),
        "last_reviews": Review.objects.all().order_by("-date_of_post")[:3],
    }