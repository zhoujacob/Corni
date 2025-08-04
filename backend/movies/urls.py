from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieAddView, MovieViewSet, TMDbPreviewView, MovieDetailView

router = DefaultRouter()
router.register("", MovieViewSet, basename="movie")

urlpatterns = [
    path("preview/", TMDbPreviewView.as_view(), name="tmdb-preview"),
    path("add/", MovieAddView.as_view(), name="movie-add"),
    path("<int:tmdb_id>/", MovieDetailView.as_view(), name="movie-detail"),
    path("", include(router.urls)),
]
