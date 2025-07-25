from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .tmdb_service import fetch_and_store_movies, fetch_movies_from_tmdb
from .models import Movie
from .serializers import MovieSerializer

class MovieSearchView(APIView):
    permission_classes = []

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if not q:
            return Response({"detail": "Query param `q` is required."},
                status=status.HTTP_400_BAD_REQUEST)
        
        fetch_and_store_movies(q)

        qs = Movie.objects.filter(title__icontains=q).order_by("-last_synced")
        data = MovieSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve movies from our local cache.
    """
    queryset = Movie.objects.all().order_by('-last_synced')
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

class TMDbPreviewView(APIView):
    permission_classes = []

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if not q:
            return Response({"detail": "Query param `q` is required."}, status=status.HTTP_400_BAD_REQUEST)

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