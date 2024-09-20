from gamesAndReviews.models import Genre


def global_variables(request):
    return {
        "genres": Genre.objects.all(),
    }