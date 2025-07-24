from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie 
        fields = ['id', 'title', 'tmdb_id', 'overview', 'poster_path', 'release_year', 'last_synced']