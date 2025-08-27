from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MovieAddView,
    MovieViewSet,
    TMDbPreviewView,
    MovieDetailView,
    MovieCompareView,
    MovieLeaderboardView,
    MyRatingsView,
    # DeleteMovieView
)

router = DefaultRouter()
router.register("", MovieViewSet, basename="movie")

urlpatterns = [
    path("preview/", TMDbPreviewView.as_view(), name="tmdb-preview"),
    path("add/", MovieAddView.as_view(), name="movie-add"),
    path("ratings/", MyRatingsView.as_view(), name="user-ratings"),
    # path("ratings/<int:tmdb_id>/", DeleteMovieView.as_view(), name="my-rating-delete"),
    path("compare/", MovieCompareView.as_view(), name="movie-compare"),
    path("leaderboard/", MovieLeaderboardView.as_view(), name="movie-leaderboard"),
    path("<int:tmdb_id>/", MovieDetailView.as_view(), name="movie-detail"),
    path("", include(router.urls)),
]
