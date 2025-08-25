from django.contrib import admin
from .models import Movie, MovieRating


class MovieRatingInline(admin.TabularInline):
    model = MovieRating
    extra = 0
    readonly_fields = ("updated",)
    autocomplete_fields = ("user",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "tmdb_id", "release_year", "last_synced")
    search_fields = ("title", "tmdb_id")
    list_filter = ("release_year",)
    inlines = [MovieRatingInline]


@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "user", "rating", "updated")
    list_select_related = ("movie", "user")
    search_fields = ("movie__title", "movie__tmdb_id", "user__email", "user__first_name", "user__last_name")
    list_filter = ("user",)
    autocomplete_fields = ("movie", "user")
    readonly_fields = ("updated",)
