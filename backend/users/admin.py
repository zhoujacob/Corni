from django.contrib import admin
from .models import CustomUser
from movies.models import MovieRating


class UserMovieRatingInline(admin.TabularInline):
    model = MovieRating
    extra = 0
    readonly_fields = ("updated",)
    autocomplete_fields = ("movie",)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser")
    readonly_fields = ("date_joined",)
    ordering = ("email",)
    inlines = [UserMovieRatingInline]
