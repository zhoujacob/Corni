from typing import TypedDict, cast
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.db.models import Avg, Count
from .tmdb_service import fetch_movie_by_id, serialize_tmdb_movie, fetch_movies_from_tmdb, get_or_fetch_movie
from .models import Movie, MovieRating
from .serializers import MovieSerializer, MovieCompareSerializer, MovieLeaderboardItemSerializer
from .elo import update_elo
from .constants import DEFAULT_ELO, K_FACTOR, BAYES_PRIOR_M

# MOVIE VIEWS
class MovieAddView(APIView):
    """
    Adds a movie to the local database using a TMDb movie ID.

    Request Body (application/json):
    {
        "tmdb_id": <int>
    }
    """
    def post(self, request):
        tmdb_id = request.data.get("tmdb_id")
        if not tmdb_id:
            return Response({"detail": "tmdb_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tmdb_id = int(tmdb_id)
        except ValueError:
            return Response({"detail": "tmdb_id must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check local DB first
        try:
            movie = Movie.objects.get(tmdb_id=tmdb_id)
            return Response({
                "source": "local",
                "movie": MovieSerializer(movie).data
            }, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            pass

        movie = fetch_movie_by_id(tmdb_id)
        movie_data = serialize_tmdb_movie(movie)

        obj, created = Movie.objects.update_or_create(
            tmdb_id=tmdb_id,
            defaults=movie_data,
        )

        return Response(MovieSerializer(obj).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve movies from our local cache.
    """
    queryset = Movie.objects.all().order_by('-last_synced')
    serializer_class = MovieSerializer

class TMDbPreviewView(APIView):
    """
    Gets all movie details given the parameter
    """

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if not q:
            return Response({"detail": "Query param `q` is required."}, status=status.HTTP_400_BAD_REQUEST)

        local_matches = Movie.objects.filter(title__icontains=q).order_by("-last_synced")
        local_serialized = MovieSerializer(local_matches, many=True).data

        # Add 'source': 'local' to local results
        results = [
            {**movie, "source": "local"}
            for movie in local_serialized
        ][:4]
    
        if len(results) < 4:
            tmdb_results = fetch_movies_from_tmdb(q)
            # Collect tmdb_ids from local results to avoid duplicates
            local_tmdb_ids = {movie.get("tmdb_id") or movie.get("id") for movie in results}
            count_needed = 4 - len(results)
            tmdb_simplified = []
            for r in tmdb_results:
                tmdb_id = getattr(r, "id", None)
                if tmdb_id not in local_tmdb_ids:
                    tmdb_simplified.append({
                        "tmdb_id": tmdb_id,
                        "title": getattr(r, "title", ""),
                        "overview": getattr(r, "overview", ""),
                        "poster_path": getattr(r, "poster_path", ""),
                        "release_date": getattr(r, "release_date", ""),
                        "source": "tmdb"
                    })
                if len(tmdb_simplified) >= count_needed:
                    break
            results.extend(tmdb_simplified)

        return Response(results, status=status.HTTP_200_OK)

class MovieDetailView(APIView):
    """
    Retrieve a movie by its TMDb ID.
    """
    def get(self, request, tmdb_id):
        try:
            tmdb_id = int(tmdb_id)
        except ValueError:
            return Response({"detail": "tmdb_id must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(tmdb_id=tmdb_id)
            return Response(MovieSerializer(movie).data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            pass

        movie = fetch_movie_by_id(tmdb_id)
        if not movie:
            return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serialize_tmdb_movie(movie), status=status.HTTP_200_OK)

class MyMoviesView(APIView):
    """
    List all movies rated by the current user, along with their ratings.
    """
    def get(self, request):
        user = request.user
        # Order by highest Elo rating first, then most recently updated
        ratings = (
            MovieRating.objects
            .filter(user=user)
            .select_related('movie')
            .order_by('-rating', '-updated')
        )
        data = [
            {
                "movie": MovieSerializer(rating.movie).data,
                "rating": round(rating.rating, 2),
                "updated": rating.updated
            }
            for rating in ratings
        ]
        return Response(data, status=status.HTTP_200_OK)

# ELO RATING VIEWS
class CompareData(TypedDict):
    movie1_id: int
    movie2_id: int
    winner_id: int

class MovieCompareView(APIView):
    """
    Submit a pairwise comparison between two movies for the current user and
    update per-user Elo ratings. Accepts TMDb IDs.

    Request Body (application/json):
    {
        "movie1_id": <int>,  # tmdb_id
        "movie2_id": <int>,  # tmdb_id
        "winner_id": <int>   # must equal movie1_id or movie2_id
    }
    """

    def post(self, request):
        serializer = MovieCompareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(CompareData, serializer.validated_data)
        m1_id = data["movie1_id"]
        m2_id = data["movie2_id"]
        winner_id = data["winner_id"]

        if m1_id == m2_id:
            return Response({"detail": "movie1_id and movie2_id must differ"}, status=status.HTTP_400_BAD_REQUEST)

        if winner_id not in (m1_id, m2_id):
            return Response({"detail": "winner_id must match movie1_id or movie2_id"}, status=status.HTTP_400_BAD_REQUEST)

        movie1 = get_or_fetch_movie(m1_id)
        movie2 = get_or_fetch_movie(m2_id)
        if not movie1 or not movie2:
            return Response({"detail": "One or both movies not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        # Get or create per-user ratings
        r1, _ = MovieRating.objects.get_or_create(user=user, movie=movie1, defaults={"rating": DEFAULT_ELO})
        r2, _ = MovieRating.objects.get_or_create(user=user, movie=movie2, defaults={"rating": DEFAULT_ELO})

        score_a = 1.0 if winner_id == m1_id else 0.0
        new_a, new_b = update_elo(r1.rating, r2.rating, score_a, k=K_FACTOR)

        r1.rating = new_a
        r2.rating = new_b
        r1.save(update_fields=["rating", "updated"])
        r2.save(update_fields=["rating", "updated"])

        return Response({
            "movie1": {"tmdb_id": movie1.tmdb_id, "rating": round(r1.rating, 2)},
            "movie2": {"tmdb_id": movie2.tmdb_id, "rating": round(r2.rating, 2)}
        }, status=status.HTTP_200_OK)


class MovieLeaderboardView(APIView):
    """
    Global leaderboard across all users based on Elo ratings.
    Returns average rating, rating count, and Bayesian-adjusted rating.

    Query params:
      - limit: max items to return (default 50)
      - min_ratings: minimum number of ratings to include (default 1)
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            limit = int(request.query_params.get("limit", 50))
            min_ratings = int(request.query_params.get("min_ratings", 1))
        except ValueError:
            return Response({"detail": "limit and min_ratings must be integers"}, status=status.HTTP_400_BAD_REQUEST)

        global_mean = MovieRating.objects.aggregate(avg=Avg("rating"))['avg'] or DEFAULT_ELO

        qs = (
            Movie.objects
            .annotate(avg_rating=Avg("movie_ratings__rating"), num_ratings=Count("movie_ratings"))
            .filter(num_ratings__gte=min_ratings)
        )

        # Compute Bayesian rating in Python, attach attribute for serializer
        items = []
        for m in qs:
            avg = cast(float, getattr(m, 'avg_rating', DEFAULT_ELO) or DEFAULT_ELO)
            n = cast(int, getattr(m, 'num_ratings', 0) or 0)
            bayes = (BAYES_PRIOR_M * global_mean + n * avg) / (BAYES_PRIOR_M + n) if n >= 0 else avg
            setattr(m, 'bayes_rating', bayes)
            items.append(m)

        # Sort by Bayesian rating desc, then by num_ratings desc
        items.sort(key=lambda x: (getattr(x, 'bayes_rating', 0), x.num_ratings or 0), reverse=True)
        items = items[:max(0, limit)]

        data = MovieLeaderboardItemSerializer(items, many=True).data
        return Response(data, status=status.HTTP_200_OK)
