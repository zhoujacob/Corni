from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .tmdb_service import fetch_movie_by_id, serialize_tmdb_movie, fetch_movies_from_tmdb
from .models import Movie
from .serializers import MovieSerializer

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
        if local_matches.exists():
            return Response({
                "source": "local",
                "results": MovieSerializer(local_matches, many=True).data
            }, status=status.HTTP_200_OK)
        
        results = fetch_movies_from_tmdb(q)

        simplified = [
            {
                "id": getattr(r, "id", None),
                "title": getattr(r, "title", ""),
                "overview": getattr(r, "overview", ""),
                "poster_path": getattr(r, "poster_path", ""),
                "release_date": getattr(r, "release_date", ""),
            }
            for r in results
        ]

        return Response(simplified, status=status.HTTP_200_OK)