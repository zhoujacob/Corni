from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieSearchView, MovieViewSet, TMDbPreviewView

router = DefaultRouter()
router.register("", MovieViewSet, basename="movie")

urlpatterns = [
    path("preview/", TMDbPreviewView.as_view(), name="tmdb-preview"),
    path("search/", MovieSearchView.as_view(), name="movie-search"),
    path("", include(router.urls)),
]
