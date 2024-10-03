from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from gamesAndReviews.models import Game, Genre, Author, Review

admin.site.register(Genre)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("genre", "release_date")


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("pseudonym",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {"fields": ("pseudonym",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "pseudonym",
                    )
                },
            ),
        )
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ("author", "date_of_post")
