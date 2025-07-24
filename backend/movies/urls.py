from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieSearchView, MovieViewSet

router = DefaultRouter()
router.register("movies", MovieViewSet, basename="movie")

urlpatterns = [
    path("search/", MovieSearchView.as_view(), name="movie-search"),
    path("", include(router.urls)),
]
