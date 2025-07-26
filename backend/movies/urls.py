from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieAddView, MovieViewSet, TMDbPreviewView

router = DefaultRouter()
router.register("", MovieViewSet, basename="movie")

urlpatterns = [
    path("preview/", TMDbPreviewView.as_view(), name="tmdb-preview"),
    path("add/", MovieAddView.as_view(), name="movie-add"),
    path("", include(router.urls)),
]
