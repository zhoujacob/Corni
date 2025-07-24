from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .tmdb_service import fetch_and_store_movies
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